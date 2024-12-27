# vsoneliner

vsoneliner generates VapourSynth script file for VSPipe from commandline. It is for the situation where only the simplest VapourSynth script is needed, and where writing and keeping a script file becomes cumbersome.  

Install vsoneliner:  
```sh
python -m pip install vsoneliner
```

An Example of using vsoneliner using [fish shell](https://fishshell.com/):  
```fish
INPUT=(realpath "input.mkv") vspipe (python -m vsoneliner "import mvsfunc as mvf" "r\"$INPUT\" |> core.lsmas.LWLibavSource |> mvf.Depth\$(depth=10) |> .set_output()") -c y4m - | x264 --demuxer y4m --output "output.mkv" -
```
Excerpt:  
```
python -m vsoneliner "import mvsfunc as mvf" "r\"$INPUT\" |> core.lsmas.LWLibavSource |> mvf.Depth\$(depth=10) |> .set_output()"
```

* Each positional argument to vsoneliner corresponds to one line in the resulting Python script. In this example, we have two lines: `import mvsfunc as mvf` and `r"INPUT" |> core.lsmas.LWLibavSource |> mvf.Depth$(depth=10) |> .set_output()`.  
* vsoneliner by default imports `from vapoursynth import core` and `import vapoursynth as vs`, but any additional imports have to be written manually, such as `import mvsfunc as mvf` in the example.  
* vsoneliner accepts [Coconut](https://coconut-lang.org/) language in the commandline. Coconut language's syntax is a strict superset of Python, which means if you don't want to learn it, you can write vanilla Python code and it will work just fine. Here in this example, `r"INPUT" |> core.lsmas.LWLibavSource |> mvf.Depth$(depth=10) |> .set_output()` transpiles to `mvf.Depth(core.lsmas.LWLibavSource(r"INPUT"), depth=10).set_output()`.  
* vsoneliner saves the commands to a Python file with `.vpy` file extension and then print the path to the file to stdout before exiting. Use `$()` in a POSIX shell to feed this file to vspipe. vsoneliner also accepts `--verbose` argument, with which vsoneliner will also print the path to the file to stderr.  
