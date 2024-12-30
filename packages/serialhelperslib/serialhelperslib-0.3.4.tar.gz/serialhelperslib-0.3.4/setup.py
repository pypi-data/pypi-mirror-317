from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=[Extension("Helpers", ["SerialHelpers/Helpers.cpython-312.pyc"]), ]
)

#
# # --- Package metadata ---
# PACKAGE_NAME = "serialhelperslib"
# VERSION = "0.2.4"
# DESCRIPTION = "A fast Cython-based package"
# AUTHOR = "Your Name"
# AUTHOR_EMAIL = "your.email@example.com"
# URL = "https://github.com/yourusername/my_cython_package"  # Your project's URL
# LICENSE = "MIT"
#
# # --- Extension modules ---
# extensions = [
#     Extension(
#         f"{PACKAGE_NAME}.mymodule",  # The full name of your extension module
#         ["SerialHelpers/helpers.pyx"],
#         # include_dirs=[numpy.get_include()],  # Add if using NumPy
#         # extra_compile_args=['-O3'],  # Optional: Add compiler optimization flags
#         # extra_link_args=['-lm'],    # Optional: Add linker flags (e.g., link to math library)
#     ),
#     # Add more Extension objects if you have multiple Cython modules
# ]
#
# # --- Setup configuration ---
# setup(
#     name=PACKAGE_NAME,
#     version=VERSION,
#     description=DESCRIPTION,
#     author=AUTHOR,
#     author_email=AUTHOR_EMAIL,
#     url=URL,
#     license=LICENSE,
#     packages=[PACKAGE_NAME],  # Find packages automatically
#     # If your package is not pure Python, you must specify
#     # where to find the shared libraries after installation:
#     package_data={
#         PACKAGE_NAME: ["*.so", "*.pyd"],  # Include .so (Linux/macOS) or .pyd (Windows) files
#     },
#     ext_modules=cythonize(
#         extensions,
#         compiler_directives={
#             "language_level": "3",  # Set Python language level
#             # "boundscheck": False,  # Optional: Disable bounds checking for performance
#             # "wraparound": False, # Optional: Disable negative indexing
#         },
#         # annotate=True,          # Optional: Generate an HTML annotation file for profiling
#     ),
#     install_requires=[
#         # "numpy",  # Add dependencies here
#         "cython", # Ensure Cython is installed for users
#     ],
#     classifiers=[
#         "Development Status :: 3 - Alpha",
#         "Intended Audience :: Developers",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3.10",
#         "Programming Language :: Python :: 3.11",
#         "Programming Language :: Python :: 3.12",
#         "Programming Language :: C",
#         "Operating System :: OS Independent",
#         "Topic :: Software Development :: Libraries :: Python Modules",
#     ],
#     python_requires=">=3.10",  # Specify minimum Python version
# )
