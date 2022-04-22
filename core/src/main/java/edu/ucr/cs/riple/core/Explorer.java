package edu.ucr.cs.riple.core;

import com.google.common.collect.ImmutableSet;
import edu.ucr.cs.riple.core.metadata.graph.FixGraph;
import edu.ucr.cs.riple.core.metadata.graph.Node;
import edu.ucr.cs.riple.core.metadata.index.Bank;
import edu.ucr.cs.riple.core.metadata.index.Error;
import edu.ucr.cs.riple.core.metadata.index.Fix;
import edu.ucr.cs.riple.core.metadata.index.Result;
import edu.ucr.cs.riple.core.metadata.method.MethodInheritanceTree;
import edu.ucr.cs.riple.core.metadata.trackers.Region;
import edu.ucr.cs.riple.core.metadata.trackers.RegionTracker;
import edu.ucr.cs.riple.core.util.Utility;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import me.tongfei.progressbar.ProgressBar;

public class Explorer {

  private final FixGraph<Node> fixGraph;
  private final RegionTracker tracker;
  private final AnnotationInjector injector;
  private final Bank<Error> errorBank;
  private final Bank<Fix> fixBank;
  private final MethodInheritanceTree methodInheritanceTree;
  private final ImmutableSet<Report> reports;
  private final Config config;

  public Explorer(
      AnnotationInjector injector,
      Bank<Error> errorBank,
      Bank<Fix> fixBank,
      RegionTracker tracker,
      MethodInheritanceTree methodInheritanceTree,
      ImmutableSet<Fix> fixes,
      Config config) {
    this.tracker = tracker;
    this.injector = injector;
    this.fixBank = fixBank;
    this.errorBank = errorBank;
    this.methodInheritanceTree = methodInheritanceTree;
    this.fixGraph = new FixGraph<>(Node::new);
    this.reports =
        fixes.stream().map(fix -> new Report(fix, -1)).collect(ImmutableSet.toImmutableSet());
    this.config = config;
  }

  private boolean init() {
    this.fixGraph.clear();
    Set<Report> filteredReports =
        this.reports
            .stream()
            .filter(report -> (!config.bailout || report.effectiveNess > 0) && !report.finished)
            .collect(Collectors.toSet());
    filteredReports.forEach(
        report -> {
          Fix root = report.root;
          Node node = fixGraph.findOrCreate(root);
          node.setRootSource(fixBank);
          node.report = report;
          node.triggered = report.triggered;
          node.tree.addAll(report.tree);
          node.mergeTriggered();
          node.updateRegions(tracker);
          node.changed = false;
        });
    return filteredReports.size() > 0;
  }

  public ImmutableSet<Report> explore() {
    System.out.println("Max Depth level: " + config.depth);
    for (int i = 0; i < config.depth; i++) {
      System.out.print("Analyzing at level " + (i + 1) + ", ");
      if (!init()) {
        break;
      }
      executeNextCycle();
      List<Node> nodes = fixGraph.getAllNodes();
      nodes.forEach(
          node -> {
            Report report = node.report;
            report.effectiveNess = node.effect;
            report.tree = node.tree;
            report.triggered = node.triggered;
            report.finished = !node.changed;
          });
    }
    return reports;
  }

  private void executeNextCycle() {
    if (fixGraph.nodes.size() == 0) {
      return;
    }
    fixGraph.findGroups(config.optimized);
    HashMap<Integer, Set<Node>> groups = fixGraph.getGroups();
    System.out.println(
        "Scheduling for: "
            + groups.size()
            + " builds for: "
            + fixGraph.getAllNodes().size()
            + " reports");
    ProgressBar pb = Utility.createProgressBar("Analysing", groups.size());
    for (Set<Node> group : groups.values()) {
      pb.step();
      Set<Fix> fixes = new HashSet<>();
      group.forEach(superNode -> fixes.addAll(superNode.getTree()));
      injector.inject(fixes);
      Utility.buildProject(config);
      errorBank.saveState(false, true);
      fixBank.saveState(false, true);
      group.forEach(
          node -> {
            int totalEffect = 0;
            List<Fix> localTriggered = new ArrayList<>();
            for (Region region : node.regions) {
              Result<Error> res = errorBank.compareByMethod(region.clazz, region.method, false);
              totalEffect += res.size;
              localTriggered.addAll(
                  new ArrayList<>(fixBank.compareByMethod(region.clazz, region.method, false).dif));
            }
            localTriggered.addAll(
                node.generateSubMethodParameterInheritanceFixes(methodInheritanceTree, fixes));
            node.updateTriggered(localTriggered);
            node.setEffect(totalEffect, methodInheritanceTree);
          });
      injector.remove(fixes);
    }
    pb.close();
  }
}