import time
import core
# vm = core.addVm({
#     "image":"debian-12"
#     })

# print(core.listVms())
# print(core.listVms("state='stopped'"))

# core.startVm(vm['id'])
# time.sleep(20)
# core.stopVm(vm['id'])
# time.sleep(20)
# core.removeVm(vm['id'])


vm = core.addVm({
    "image":"debian-12"
    })
core.startVm(vm['id'])
time.sleep(20)
core.removeVm(vm['id'])
