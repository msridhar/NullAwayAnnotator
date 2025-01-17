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

package edu.ucr.cs.riple.core.tools;

import edu.ucr.cs.riple.core.Report;
import edu.ucr.cs.riple.core.metadata.index.Fix;
import edu.ucr.cs.riple.injector.Change;
import edu.ucr.cs.riple.injector.location.Location;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import javax.annotation.Nullable;

/** Wrapper class for {@link Report} with default values, used to create tests. */
public class TReport extends Report {
  public TReport(Location root, int effect) {
    this(root, effect, "", "");
  }

  public TReport(Location root, int effect, String encClass, String encMethod) {
    super(
        new Fix(new Change(root, "javax.annotation.Nullable", true), null, encClass, encMethod),
        effect);
  }

  public TReport(
      Location root,
      int effect,
      @Nullable Set<Location> addToTree,
      @Nullable Set<Location> triggered) {
    this(root, effect);
    if (triggered != null) {
      this.triggered =
          triggered.stream().map((Function<Location, Fix>) TFix::new).collect(Collectors.toSet());
    }
    if (addToTree != null) {
      this.tree.addAll(
          addToTree.stream().map((Function<Location, Fix>) TFix::new).collect(Collectors.toSet()));
    }
  }
}
