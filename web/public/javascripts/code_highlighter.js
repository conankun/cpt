    var cm = CodeMirror(document.getElementById("editor"), {
      value: "#include<stdio.h>\nint main(){\n  int a,b;\n  scanf(\"%d%d\",&a,&b);\n  printf(\"%d\", a+b);\n}",
      indentUnit: 4,
      lineNumbers: true,
      matchBrackets: true,
      styleActiveLine: true,
      mode: "text/x-c++src"
    });
    var terminal = CodeMirror(document.getElementById("terminal"), {
       value: "Test Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\nTest Case #1..........ok\nTest Case #2..........ok\n",
       readOnly: true,
       styleActiveLine: true,
       mode: "text",
       keyMap: "sublime",
       theme: "monokai"
    });
    var mac = CodeMirror.keyMap.default == CodeMirror.keyMap.macDefault;
    CodeMirror.keyMap.default[(mac ? "Cmd" : "Ctrl") + "-Space"] = "autocomplete";

