/*
 * MIT License
 *
 * Copyright (c) 2020 Nima Karimipour
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package edu.ucr.cs.riple.core.metadata.trackers;

import edu.ucr.cs.riple.core.metadata.MetaData;
import edu.ucr.cs.riple.core.metadata.index.Fix;
import edu.ucr.cs.riple.core.metadata.method.MethodInheritanceTree;
import edu.ucr.cs.riple.core.metadata.method.MethodNode;
import edu.ucr.cs.riple.injector.location.OnMethod;
import java.nio.file.Path;
import java.util.Set;
import java.util.stream.Collectors;

public class MethodRegionTracker extends MetaData<TrackerNode> implements RegionTracker {

  private final MethodInheritanceTree tree;

  public MethodRegionTracker(Path path, MethodInheritanceTree tree) {
    super(path);
    this.tree = tree;
  }

  @Override
  protected TrackerNode addNodeByLine(String[] values) {
    return new TrackerNode(values[0], values[1], values[2], values[3]);
  }

  @Override
  public Set<Region> getRegions(Fix fix) {
    if (!fix.isOnMethod()) {
      return null;
    }
    OnMethod onMethod = fix.toMethod();
    Set<Region> regions = getCallersOfMethod(onMethod.clazz, onMethod.method);
    MethodNode parent = tree.getSuperMethod(onMethod.method, onMethod.clazz);
    if (parent != null) {
      regions.add(new Region(parent.method, parent.clazz));
    }
    return regions;
  }

  public Set<Region> getCallersOfMethod(String clazz, String method) {
    return findAllNodes(
            candidate ->
                candidate.calleeClass.equals(clazz) && candidate.calleeMember.equals(method),
            clazz)
        .stream()
        .map(node -> new Region(node.callerMethod, node.callerClass))
        .collect(Collectors.toSet());
  }
}
