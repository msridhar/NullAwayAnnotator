package edu.ucr.cs.riple.core.metadata.field;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class FieldDeclarationInfo {
  public final Set<Set<String>> fields;
  public final String clazz;

  public FieldDeclarationInfo(String clazz) {
    this.clazz = clazz;
    this.fields = new HashSet<>();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof FieldDeclarationInfo)) return false;
    FieldDeclarationInfo info = (FieldDeclarationInfo) o;
    return clazz.equals(info.clazz);
  }

  @Override
  public int hashCode() {
    return Objects.hash(clazz);
  }

  public int size() {
    return this.fields.size();
  }

  public void addNewSetOfFieldDeclarations(Set<String> collection) {
    this.fields.add(collection);
  }
}
