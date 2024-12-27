# pylcs-rs

This is a Rust port of the [pylcs](https://github.com/Meteorix/pylcs) project.

## benchmark

on M4 MacOS

```
$ docker build -t lcsbench -f benchmark.dockerfile.aarch64 .
$ docker run -it --rm lcsbench
```

```
Input Sizes                    | pylcs_rs            | pylcs
------------------------------------------------------------------------
(3, 7)                         | 0.000001 ±0.000001 | 0.000001 ±0.000002
(5, 3)                         | 0.000001 ±0.000001 | 0.000001 ±0.000000
(1000, 1100)                   | 0.003899 ±0.000217 | 0.002706 ±0.000069
(1500, 1500)                   | 0.008471 ±0.000209 | 0.005510 ±0.000138
(1100, 1100)                   | 0.003577 ±0.000050 | 0.002596 ±0.000030
(520, 520)                     | 0.000800 ±0.000047 | 0.000569 ±0.000013
```

## development

Build and Test Rust Modules

```
cargo test
```

Install dev dependencies

```
uv sync
```

Build for editable package

```
uv run maturin develop --uv
```

Test Python Module

```
uv run pytest
```

build for release

```
uv run maturin build --release
```

The Artifact should be like: `./target/wheels/pylcs_rs-0.1.0-cp312-cp312-*.whl`
