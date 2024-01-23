## Conan Recipes


### What is it?

The recipes in this repo contain common code that can be reused in conanfiles via the **python_requires** mechanism in either [conan v1](https://docs.conan.io/en/1.62/extending/python_requires.html) or [conan v2](https://docs.conan.io/2.0/reference/extensions/python_requires.html) mechanism. It is intended for use in either the conan based CI or local conan based build.

### How to setup

It's recommended that this repo be set as a submodule in the repo. e.g. in ./external/conan-recipes. Other solutions are possible and left to the reader.

### What recipe packages are available?

The package recipes supported are:

#### 1. Bundled package - for multi-build type packages

1. Purpose: 

> To provide a mechanism for performing several individual build type `conan create` and then packaging all the build types into a single package . 

2. For example: 

```sh
    conan export ./external/conan-recipes/bundle_package bundleutils/0.1@lkeb/stable
    conan create . <pkg_name>/<n.n.n>@<user/channel> -pr:h profile -pr:b profile
    conan create . <pkg_name>/<n.n.n>@<user/channel> -pr:h profile -pr:b profile -s build_type=Debug -o merge_package=True
```

The default merge settings are : 

```
    _merge_from = ["Debug", "RelWithDebInfo"]
    _merge_to = "Release"
```
3. In the consumer `conanfile.py`


however they can be overridden in the consumer conanfile. 

Add a call to `self._merge_packages()` at the end of the conan `package` method to trigger the copy

