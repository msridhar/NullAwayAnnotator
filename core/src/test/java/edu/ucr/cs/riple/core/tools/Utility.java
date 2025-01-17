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

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Objects;

public class Utility {

  public static Path getPathOfResource(String relativePath) {
    return Paths.get(
        Objects.requireNonNull(Utility.class.getClassLoader().getResource(relativePath)).getFile());
  }

  public static String changeDirCommand(String path) {
    String os = System.getProperty("os.name").toLowerCase();
    return (os.startsWith("windows") ? "dir" : "cd") + " " + path;
  }

  public static ProcessBuilder createProcessInstance() {
    ProcessBuilder pb = new ProcessBuilder();
    String os = System.getProperty("os.name").toLowerCase();
    return os.startsWith("windows") ? pb.command("cmd.exe", "/c") : pb.command("bash", "-c");
  }
}
