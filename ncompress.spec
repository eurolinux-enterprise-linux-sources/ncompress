Summary: Fast compression and decompression utilities
Name: ncompress
Version: 4.2.4.4
Release: 1%{?dist}
License: Public Domain
Group:  Applications/File
URL:    http://ncompress.sourceforge.net/
Source: http://prdownloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz

# allow to build ncompress
# ~> downstream
Patch0: ncompress-4.2.4.4-make.patch

# from dist-git commit 0539779d937
# (praiskup: removed redundant part as -DNOFUNCDEF is defined)
# ~> downstream
Patch1: ncompress-4.2.4.4-lfs.patch

# exit when too long filename is given (do not segfault)
# ~> #unknown
# ~> downstream
Patch2: ncompress-4.2.4.4-filenamelen.patch

# permit files > 2GB to be compressed
# ~> #126775
Patch3: ncompress-4.2.4.4-2GB.patch

# do not fail to compress on ppc/s390x
# ~> #207001
Patch4: ncompress-4.2.4.4-endians.patch

# use memmove instead of memcpy
# ~> 760657
# ~> downstream
Patch5: ncompress-4.2.4.4-memmove.patch

# silence gcc warnings
# ~> downstream
Patch6: ncompress-4.2.4.4-silence-gcc.patch

BuildRequires: glibc-devel fileutils

%description
The ncompress package contains the compress and uncompress file
compression and decompression utilities, which are compatible with the
original UNIX compress utility (.Z file extensions).  These utilities
can't handle gzipped (.gz file extensions) files, but gzip can handle
compressed files.

Install ncompress if you need compression/decompression utilities
which are compatible with the original UNIX compress utility.

%prep
%setup -q

# configure build system
# ~> downstream
%patch0 -p1 -b .configure-buildsystem

%ifarch sparc m68k armv4l ppc s390 s390x ppc64 sparc64
ARCH_FLAGS="$ARCH_FLAGS -DBYTEORDER=1234"
%endif

%ifarch alpha ia64
ARCH_FLAGS="$ARCH_FLAGS -DNOALLIGN=0"
%endif

sed "s/\$(ARCH_FLAGS)/$ARCH_FLAGS/" Makefile.def > Makefile

%patch1 -p1 -b .lfs
%patch2 -p1 -b .filenamelen
%patch3 -p1 -b .2GB
%patch4 -p1 -b .endians
%patch5 -p1 -b .memmove
%patch6 -p1 -b .silence-gcc

%build
make CFLAGS="%{optflags} %{?nc_endian} %{?nc_align}"

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m755 compress $RPM_BUILD_ROOT/%{_bindir}
ln -sf compress $RPM_BUILD_ROOT/%{_bindir}/uncompress
install -p -m644 compress.1 $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf compress.1 $RPM_BUILD_ROOT%{_mandir}/man1/uncompress.1

%files
%{_bindir}/compress
%{_bindir}/uncompress
%{_mandir}/man1/*
%doc LZW.INFO README

%changelog
* Fri Mar 01 2013 Pavel Raiskup <praiskup@redhat.com> - 4.2.4.4-1
- upstream is dead -> rebase to fork of Mike Frysinger
- silence gcc warnings, fedora-review fixes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-56
- use memmove instead of memcpy to prevent memory overlap corruption
 (#760657)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-54
- do patch original Makefile.def instead of creating new Makefile

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ondrej Vasik <ovasik@redhat.com> - 4.2.4-51
- check malloc success (#473488)
- fix few compiler warnings, free malloc memory before exit
- new URL

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.2.4-50
- Autorebuild for GCC 4.3

* Fri Feb 09 2007 Peter Vrabec <pvrabec@redhat.com> 4.2.4-49
- fix spec file to meet Fedora standards (#226185) 

* Wed Jan 10 2007 Peter Vrabec <pvrabec@redhat.com> 4.2.4-48
- fix some rpmlint issues

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-47
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-46
- fix endian problem (#207001)

* Thu Aug 10 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-45
- fix bss buffer underflow CVE-2006-1168 (#201919)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-44.1
- rebuild

* Fri Apr 21 2006 Peter Vrabec <pvrabec@redhat.com> 4.2.4-44
- fix problems with compressing zero-sized files (#189215, #189216)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.2.4-43.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep 22 2005 Peter Vrabec <pvrabec@redhat.com> 4.2.4-43
- compress zero-sized files when -f is used(#167615)

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Thu Feb 08 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Tue Oct 05 2004 Than Ngo <than@redhat.com> 4.2.4-40
- permit files > 2GB to be compressed (#126775).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 4.2.4-32
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-30
- Don't strip when installing

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Feb 27 2002 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-28
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 26 2001 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-26
- Rebuild, to fix problem with broken man page (#56654)

* Wed Nov 21 2001 Trond Eivind Glomsrod <teg@redhat.com> 4.2.4-25
- Exit, don't segfault, when given too long filenames

* Sat Jun 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- s390x change

* Tue May  8 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Make it support large files (structs, stats, opens and of course:
  _don't use signed longs for file size before and after compression_.)
  This should fix #39470

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x, patch from Oliver Paukstadt <oliver.paukstadt@millenux.com>

* Mon Nov 13 2000 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- add s390 to the bigendian arch list

* Thu Aug 17 2000 Trond Eivind Glomsrod <teg@redhat.com>
- change category to Applications/File, to match
  gzip and bzip2 
- rename the spec file to ncompress.spec
- add ppc to the bigendian arch list

* Fri Jul 21 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrod <teg@redhat.com>
- update URL
- use %%{_mandir}

* Wed May  5 2000 Bill Nottingham <notting@redhat.com>
- fix "build" for ia64

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- build on armv4l too
- build for 6.0

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
