import libvirt

con = libvirt.open("qemu+ssh://alumno@node2/system")
doms = con.listAllDomains()
print(doms)
# for dom in doms: print(dom.ID())
# dom = con.lookupByName(name)
# dom = con.createXML(template, 0) # crea y arranca una máquina virtual
# dom.shutdown()
# dom.destroy()