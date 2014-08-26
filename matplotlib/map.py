#!/usr/bin/env python
from myplot import latinterv, define_proj, makeplotres
[wlon,wlat] = latinterv("Africa")
define_proj("ortho",wlon,wlat,back="blueclouds")
makeplotres("blueclouds",ext='ps')
define_proj("ortho",wlon,wlat,back="blue")
makeplotres("blue",ext='ps')
define_proj("ortho",wlon,wlat,back="justclouds")
makeplotres("justclouds",ext='ps')

