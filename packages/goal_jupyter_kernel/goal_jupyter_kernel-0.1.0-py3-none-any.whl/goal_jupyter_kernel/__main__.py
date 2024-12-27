from ipykernel.kernelapp import IPKernelApp

from . import GoalKernel

IPKernelApp.launch_instance(kernel_class=GoalKernel)
