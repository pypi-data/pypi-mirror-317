#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(python_example_wierdre, m) {
    m.def("add", add, "add function");
}