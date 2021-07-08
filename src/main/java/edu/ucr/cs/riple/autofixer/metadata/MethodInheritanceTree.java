package edu.ucr.cs.riple.autofixer.metadata;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class MethodInheritanceTree extends AbstractRelation<MethodNode>{
    HashMap<Integer, MethodNode> nodes;

    public MethodInheritanceTree(String filePath) {
        super(filePath);
        nodes = new HashMap<>();
    }

    @Override
    protected MethodNode addNodeByLine(String[] values) {
        Integer id = Integer.parseInt(values[0]);
        MethodNode node;
        if (nodes.containsKey(id)) {
            node = nodes.get(id);
        } else {
            node = new MethodNode();
            nodes.put(id, node);
        }
        Integer parentId = Integer.parseInt(values[3]);
        node.fillInformation(id, values[1], values[2], values[5], parentId);
        if (parentId != -1) {
            MethodNode parent = nodes.get(parentId);
            if (parent == null) {
                parent = new MethodNode();
                nodes.put(parentId, parent);
            }
            parent.addChild(id);
        }
        return node;
    }

    public List<MethodNode> getSuperMethods(String method, String clazz) {
        List<MethodNode> ans = new ArrayList<>();
        MethodNode node = findNode((candidate, values) -> candidate.method.equals(values[0]) && candidate.clazz.equals(values[1]), method, clazz);
        if (node == null) {
            return ans;
        }
        while (node != null) {
            MethodNode parent = nodes.get(node.parent);
            if (parent != null) {
                ans.add(parent);
            }
            node = parent;
        }
        return ans;
    }

    public List<MethodNode> getSubMethods(String method, String clazz){
        List<MethodNode> ans = new ArrayList<>();
        MethodNode node = findNode((candidate, values) -> candidate.method.equals(values[0]) && candidate.clazz.equals(values[1]), method, clazz);
        if(node == null) {
            return ans;
        }
        if(node.children == null){
            return ans;
        }
        Set<Integer> workList = new HashSet<>(node.children);
        while (!workList.isEmpty()){
            Set<Integer> tmp = new HashSet<>();
            for(Integer id: workList){
                MethodNode selected = nodes.get(id);
                if(!ans.contains(selected)){
                    ans.add(selected);
                    if(selected.children != null) {
                        tmp.addAll(selected.children);
                    }
                }
            }
            workList.clear();
            workList.addAll(tmp);
        }
        return ans;
    }
}
