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

package edu.ucr.cs.riple.injector;

import edu.ucr.cs.riple.injector.location.OnMethod;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public class BasicTest extends BaseInjectorTest {

  @Test
  public void skip_duplicate_annotation() {
    Change Change =
        new Change(
            new OnMethod("Super.java", "com.uber.Super", "test()"),
            "javax.annotation.Nullable",
            true);
    injectorTestHelper
        .addInput(
            "Super.java",
            "package com.uber;",
            "import javax.annotation.Nullable;",
            "public class Super {",
            "   @Nullable Object test() {",
            "       return new Object();",
            "   }",
            "}")
        .expectOutput(
            "package com.uber;",
            "import javax.annotation.Nullable;",
            "public class Super {",
            "   @Nullable Object test() {",
            "       return new Object();",
            "   }",
            "}")
        .addChanges(Change, Change.duplicate(), Change.duplicate())
        .start();
  }

  @Test
  public void skip_existing_annotations() {
    injectorTestHelper
        .addInput(
            "Super.java",
            "package com.uber;",
            "import javax.annotation.Nullable;",
            "public class Super {",
            "   Object test(@javax.annotation.Nullable Object o) {",
            "   }",
            "}")
        .expectOutput(
            "package com.uber;",
            "import javax.annotation.Nullable;",
            "public class Super {",
            "   @Nullable Object test(@javax.annotation.Nullable Object o) {",
            "   }",
            "}")
        .addChanges(
            new Change(
                new OnMethod(
                    "Super.java",
                    "com.uber.Super",
                    "test(@javax.annotation.Nullable java.lang.Object)"),
                "javax.annotation.Nullable",
                true))
        .start();
  }

  @Test
  public void custom_nullable_already_exists() {
    injectorTestHelper
        .addInput(
            "Main.java",
            "package com.uber;",
            "import custom.Nullable;",
            "public class Main {",
            "   public enum Test{",
            "     CLASSIC;",
            "     public Object run(){",
            "       return null;",
            "     }",
            "   }",
            "}")
        .expectOutput(
            "package com.uber;",
            "import custom.Nullable;",
            "public class Main {",
            "   public enum Test{",
            "     CLASSIC;",
            "     @Nullable",
            "     public Object run(){",
            "       return null;",
            "     }",
            "   }",
            "}")
        .addChanges(
            new Change(
                new OnMethod("Main.java", "com.uber.Main$Test", "run()"),
                "javax.annotation.Nullable",
                true))
        .start();
  }

  @Test
  public void custom_nullable_already_exists_part2() {
    injectorTestHelper
        .addInput(
            "Main.java",
            "package com.uber;",
            "import custom.aNullable;",
            "public class Main {",
            "   public enum Test{",
            "     CLASSIC;",
            "     public Object run(){",
            "       return null;",
            "     }",
            "   }",
            "}")
        .expectOutput(
            "package com.uber;",
            "import javax.annotation.Nullable;",
            "import custom.aNullable;",
            "public class Main {",
            "   public enum Test{",
            "     CLASSIC;",
            "     @Nullable",
            "     public Object run(){",
            "       return null;",
            "     }",
            "   }",
            "}")
        .addChanges(
            new Change(
                new OnMethod("Main.java", "com.uber.Main$Test", "run()"),
                "javax.annotation.Nullable",
                true))
        .start();
  }
}
