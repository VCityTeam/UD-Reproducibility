# What the workflow needs to express 

We here collect some needs that some workflow description technology should adress.
Such needs arised when realizing the (possibly specific) [LyonTemporal](https://github.com/VCityTeam/UD-Reproducibility/tree/master/Computations/3DTiles/LyonTemporal) particular workflow.

## Concerning the input/output file mapping

### Download and sanitize classes

- [Demo](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/demo.py)
  - `create_output_dir()`
  - `get_output_dir()`
  - `set_results_dir(results_dir)`
  - `set/get_input_demo()`: hooks up upstream container in order to obtain the
    resulting filenames for each pair of `(vintage, borough`

- [DemoWithFileOutput](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/demo.py)
  - `assert_output_files_exist(()`

- [DemoWithFileOutputTemporal(Demo, DemoWithFileOutput)](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/DemoTemporal/demo_temporal.py):
  - ```python
    __init__(results_dir = None,
             all_demos_output_dir,
             vintages,
             boroughs):
    ```
  - `get_vintage_borough_output_directory_name(vintage, borough)`
  - `get_vintage_borough_output_filename(vintage, borough)`

- [DemoLyonMetropoleDowloadAndSanitize](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/demo_lyon_metropole_dowload_and_sanitize.py)
  - constructor enables the selection of the sub-type of the Urban model that must be extracted
  - `define_vintage_borough_archive(vintage, borough)` maps a
    `(vintage, borough)` pair to the URL corresponding to that data
  - the `archives_to_sanitize()` method set's up the list of archives that must
    be patched (and how to patch them)
  - the `run()` methods loops over the configured archives
  - `get_vintage_borough_output_file_basename(vintage, borough)` maps
    `(vintage, borough)` pair to the basename of a the corresponding file
- [DemoLyonMetropoleDowloadAndSanitizeTemporal(DemoWithFileOutputTemporal, DemoLyonMetropoleDowloadAndSanitize)](https://github.com/VCityTeam/UD-Reproducibility/blob/master/Computations/3DTiles/LyonTemporal/PythonCallingDocker/DemoTemporal/demo_lyon_metropole_dowload_and_sanitize_temporal.py)
  - `define_archives()` loops over the argument vintages and loops over the
  - `get_resulting_filenames()` after asserting their existence returns the list
    of filenames relative to the numerical experiment directory. Note: this 
    method is NOT used by the downstream container.

**Conclusion** about the design choices for the input/output mapping logic

- each container wrapper is responsible for defining its naming convention of
  its out filenames. Each output filename may be tagged with a string
  designating the container role (e.g. `_split_` or `_compressed_`) as well as
  the ad-hoc filename extension (xml, yaml...)
- each output is not only a file but can be a full directory tree structure
  with sub-files...
- its internal directory tree structure (rooted at
  `experiment_root/stage_<number>` that is parametrized through the constructor)
  is encapsulated (hidden away). The downstream container shall retrieve its
  inputs by concatenating calls to
  - `get_vintage_borough_output_directory_name(vintage, borough)`
  - `get_vintage_borough_output_filename(vintage, borough)`
- each container loops over the cartesian product of argument `vintages` and
  argument `boroughs` to generate what to treat and refers to the upstream
  container 


