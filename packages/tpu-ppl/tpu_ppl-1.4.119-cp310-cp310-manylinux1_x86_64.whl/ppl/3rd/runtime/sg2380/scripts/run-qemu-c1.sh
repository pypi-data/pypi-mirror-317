#!/bin/bash

if test $# -eq 0
then
    echo "usage: $0 -kernel firmware_elf [qemu_additional_args ...]" >&2
    exit 1
fi

gdb=
if test -n "$GDB"
then
    gdb='gdb -q --args'
fi

eval $gdb qemu-system-riscv64 \
	-M sifive-base \
	-cpu rv64 \
	-smp 1 \
	-device rv64-riscv-cpu,i=true,e=false,g=false,m=true,a=true,f=true,d=true,c=true,s=true,u=true,h=false,v=true,pmp=true,mmu=true,sscofpmf=true,Zicbom=false,Zicbop=true,Zicboz=false,Zicsr=true,Zifencei=true,Zihintpause=false,Zfh=true,Zfhmin=false,Zve32f=false,Zve64f=false,sstc=false,smstateen=false,svade=false,svinval=false,svnapot=false,svpbmt=false,zba=true,zbb=true,zbc=false,zbkb=false,zbkc=false,zbkx=false,zbs=false,zca=false,zcb=false,zcd=false,zce=false,zcf=false,zcmp=false,zcmt=false,zk=false,zkn=false,zknd=false,zkne=false,zknh=false,zkr=false,zks=false,zksed=false,zksh=false,zkt=false,zdinx=false,zfinx=false,zhinx=false,zhinxmin=false,zmmul=false,x-zvbb=false,x-zvbc=false,x-zvkg=false,x-zvkn=false,x-zvknc=false,x-zvkned=false,x-zvkng=false,x-zvknha=false,x-zvknhb=false,x-zvks=false,x-zvksc=false,x-zvksed=false,x-zvksg=false,x-zvksh=false,x-zvkt=false,x-xsfvfhbfmin=true,x-xsfvfnrclipxfqf=true,x-xsfvfwmaccqqq=true,x-xsfvqmaccqoq=true,x-xsfvqmaccdod=false,x-xsfvcp=true,x-smaia=false,x-ssaia=false,x-Zvamo=false,x-Zvfh=false,x-xsifivecdiscarddlone=false,x-xsifivecflushdlone=false,vext_spec=v1.0,vlen=512,elen=64,sv48=true,beu=true,debug=true,resetvec=0x10004,id=riscv_hart0 \
	-device riscv-cpu.config,cpu=riscv_hart0,mhartid=0 \
	-device system-memory,id=memory_80000000,size=0x20000000 \
	-device sysbus-mmio-mapping,sysdev=memory_80000000,index=0,addr=0x80000000 \
	-device riscv.sifive.smc,id=soc.subsystemMC_3100000,timebase-freq=32500000,num-harts=1 \
	-device sysbus-mmio-mapping,sysdev=soc.subsystemMC_3100000,index=0,addr=0x3100000 \
	-device riscv.sifive.tmc,id=soc.subsystemMC_3100000.tmc,num-harts=1 \
	-device sysbus-mmio-mapping,sysdev=soc.subsystemMC_3100000.tmc,index=0,addr=0x3101000 \
	-device system-memory,id=soc.axi4-periph-port_20000000.testram_20000000,size=0x20000000 \
	-device sysbus-mmio-mapping,sysdev=soc.axi4-periph-port_20000000.testram_20000000,index=0,addr=0x20000000 \
	-device system-memory,id=soc.axi4-sys-port_40000000.testram_40000000,size=0x20000000 \
	-device sysbus-mmio-mapping,sysdev=soc.axi4-sys-port_40000000.testram_40000000,index=0,addr=0x40000000 \
	-device unimplemented-device,id=soc.burst-bundler_10010000,size=0x1000,name=soc.burst-bundler_10010000 \
	-device sysbus-mmio-mapping,sysdev=soc.burst-bundler_10010000,index=0,addr=0x10010000 \
	-device unimplemented-device,id=soc.burst-bundler_10040000,size=0x1000,name=soc.burst-bundler_10040000 \
	-device sysbus-mmio-mapping,sysdev=soc.burst-bundler_10040000,index=0,addr=0x10040000 \
	-device sifive,,buserror0,id=soc.bus-error-unit_1700000,legacy-local=true,mmio-size=0x1000,hartid=0 \
	-device sysbus-mmio-mapping,sysdev=soc.bus-error-unit_1700000,index=0,addr=0x1700000 \
	-device sifive_ccache,id=soc.cache-controller_2010000,cache-block-size=64,cache-sets=8192,cache-size=8388608,bank-count=8,ecc-granularity=8 \
	-device sysbus-mmio-mapping,sysdev=soc.cache-controller_2010000,index=0,addr=0x2010000 \
	-device riscv.aclint.mtimer,id=soc.clint_2000000,hartid-base=0,timecmp-base=0x0,time-base=0x7ff8,timebase-freq=1000000,num-harts=1,aperture-size=0xc000 \
	-device sysbus-mmio-mapping,sysdev=soc.clint_2000000,index=0,addr=0x2004000 \
	-device riscv.aclint.swi,id=soc.clint_2000000_mswi,hartid-base=0,sswi=0,num-harts=1 \
	-device sysbus-mmio-mapping,sysdev=soc.clint_2000000_mswi,index=0,addr=0x2000000 \
	-device sifive,,error0,id=soc.error-device_3000,mmio-size=0x1000 \
	-device sysbus-mmio-mapping,sysdev=soc.error-device_3000,index=0,addr=0x3000 \
	-device riscv.sifive.plic,id=soc.interrupt-controller_c000000,hartid-base=0,priority-base=0x4,pending-base=0x1000,enable-base=0x2000,enable-stride=0x80,context-base=0x200000,context-stride=0x1000,num-priorities=7,num-sources=141,aperture-size=0x4000000,hart-config=MS,disable-clk-gate-base=2093056 \
	-device sysbus-mmio-mapping,sysdev=soc.interrupt-controller_c000000,index=0,addr=0xc000000 \
	-device sifive.l2pf,id=soc.l2pf_2030000 \
	-device sysbus-mmio-mapping,sysdev=soc.l2pf_2030000,index=0,addr=0x2030000 \
	-device unimplemented-device,id=soc.order-obliterator_10030000,size=0x4000,name=soc.order-obliterator_10030000 \
	-device sysbus-mmio-mapping,sysdev=soc.order-obliterator_10030000,index=0,addr=0x10030000 \
	-device sifive,,pL2Cache,id=soc.pl2_10104000,cache-block-size=64,cache-sets=512,cache-size=262144,version=0 \
	-device sysbus-mmio-mapping,sysdev=soc.pl2_10104000,index=0,addr=0x10104000 \
	-device system-memory,id=soc.zerodevice_a000000,readonly=true,size=0x800000 \
	-device sysbus-mmio-mapping,sysdev=soc.zerodevice_a000000,index=0,addr=0xa000000 \
	-device riscv.sifive.test,id=soc.teststatus_4000,vcp=true,chardev=serial0 \
	-device sysbus-mmio-mapping,sysdev=soc.teststatus_4000,index=0,addr=0x4000 \
	-device unimplemented-device,id=soc.trace-encoder-0_10000000,size=0x1000,name=soc.trace-encoder-0_10000000 \
	-device sysbus-mmio-mapping,sysdev=soc.trace-encoder-0_10000000,index=0,addr=0x10000000 \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.subsystemMC_3100000 \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.subsystemMC_3100000.tmc \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.cache-controller_2010000 \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.clint_2000000 \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.clint_2000000_mswi \
	-device riscv.sifive.smc.register.device,smc-dev=soc.subsystemMC_3100000,device=soc.interrupt-controller_c000000 \
	-device riscv.sifive.tmc.register.device,tmc-dev=soc.subsystemMC_3100000.tmc,device=soc.bus-error-unit_1700000,hartid=0 \
	-device riscv.sifive.tmc.register.device,tmc-dev=soc.subsystemMC_3100000.tmc,device=soc.pl2_10104000,hartid=0 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000.tmc,input-name=reset_tile_devs,input-number=0,output-device=soc.subsystemMC_3100000,output-name=reset_tile_devs,output-number=0 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000.tmc,input-name=tmc_cpu_sleep,input-number=0,output-device=soc.subsystemMC_3100000,output-name=tmc_cpu_sleep,output-number=0 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000,input-name=wake_power_state,input-number=0,output-device=soc.subsystemMC_3100000.tmc,output-name=wake_power_state,output-number=0 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000,input-name=cpu_sleep_cease,input-number=0,output-device=riscv_hart0,output-number=0 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000,input-name=cpu_sleep_wfi,input-number=0,output-device=riscv_hart0,output-number=1 \
	-device gpio-connection,input-device=soc.subsystemMC_3100000.tmc,input-name=tmc_wake_irq,input-number=0,output-device=riscv_hart0,output-number=2 \
	-device gpio-connection,output-device=soc.interrupt-controller_c000000,output-name=wakeup_irq,output-number=0,input-device=soc.subsystemMC_3100000,input-name=smc_wake_irq,input-number=0 \
	-device sifive.buserror0.connection,beu-device=soc.bus-error-unit_1700000,hartid=0 \
	-device gpio-connection,input-device=soc.interrupt-controller_c000000,input-number=133,output-device=soc.bus-error-unit_1700000,output-number=0,output-name=beu_plic_irq \
	-device gpio-connection,input-device=riscv_hart0,input-name=riscv.cpu.rnmi,input-number=3,output-device=soc.bus-error-unit_1700000,output-name=beu_rnmi,output-number=0 \
	-device gpio-connection,input-device=riscv_hart0,input-name=riscv.cpu.beu.irq,input-number=0,output-device=soc.bus-error-unit_1700000,output-name=beu_legacy_irq,output-number=0 \
	-device gpio-connection,input-device=soc.interrupt-controller_c000000,input-number=1,output-device=soc.cache-controller_2010000,output-number=0,output-name=sysbus-irq \
	-device gpio-connection,input-device=soc.interrupt-controller_c000000,input-number=2,output-device=soc.cache-controller_2010000,output-number=1,output-name=sysbus-irq \
	-device gpio-connection,input-device=soc.interrupt-controller_c000000,input-number=3,output-device=soc.cache-controller_2010000,output-number=2,output-name=sysbus-irq \
	-device gpio-connection,input-device=soc.interrupt-controller_c000000,input-number=4,output-device=soc.cache-controller_2010000,output-number=3,output-name=sysbus-irq \
	-device gpio-connection,input-device=riscv_hart0,input-number=7,output-device=soc.clint_2000000,output-number=0 \
	-device gpio-connection,input-device=riscv_hart0,input-number=3,output-device=soc.clint_2000000_mswi,output-number=0 \
	-device gpio-connection,input-device=riscv_hart0,input-number=9,output-device=soc.interrupt-controller_c000000,output-number=0 \
	-device sifive.cpu.postinit \
	-device sifive-loader-cfg,id=loader-cfg,mrom-base=0x10000,mrom-size=0x4000,dram-base=0x80000000,dram-size=0x20000000 \
	-device sifive-loader,msel=4 -nographic  \
	"$@"
