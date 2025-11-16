---- luapstricks-plugin-pstcie.lua
-- Copyright 2021--2023 Marcel Krüger <tex@2krueger.de>
-- Converted from PostScript in pst-cie.pro version 0.03
--
-- This work may be distributed and/or modified under the
-- conditions of the LaTeX Project Public License, either version 1.3
-- of this license or (at your option) any later version.
-- The latest version of this license is in
--   http://www.latex-project.org/lppl.txt
-- and version 1.3 or later is part of all distributions of LaTeX
-- version 2005/12/01 or later.
--
-- This work has the LPPL maintenance status `maintained'.
-- 
-- The Current Maintainer of this work is M. Krüger
--
-- This work consists of the files luapstricks.lua and luapstricks-plugin-pstmarble.lua

local loader, version, plugininterface = ...
assert(loader == 'luapstricks' and version == 0)

local push = plugininterface.push
local pop = plugininterface.pop
local pop_array = plugininterface.pop_array
local pop_num = plugininterface.pop_num
local pop_proc = plugininterface.pop_proc
local pop_string = pop
local exec = plugininterface.exec

local newtable = lua.newtable
local abs = math.abs
local exp = math.exp
local cos = math.cos
local sin = math.sin
local rad = math.rad
local max = math.max
local deg = math.deg
local atan = math.atan

-- Using the usual scale
--[[
local function BLKBOD(temp, table)
  local X, Y, Z = 0, 0, 0
  for i = 1, #table do
    local WL = (359 + i) * 1e-9
    local DIS = (3.74183e-16 / WL^5) / (exp(1.4388e-2 / (WL * temp)) - 1)
    local entry = table[i]
    X = X + entry[1] * DIS
    Y = Y + entry[2] * DIS
    Z = Z + entry[3] * DIS
  end
  local XYZ = X + Y + Z
  return X / XYZ, Y / XYZ, Z / XYZ
end
--]]
-- But we can scale all components with fixed factors, so we get the same result with
local function BLKBOD(temp, table)
  assert(#table == 471) -- 471 = 830 - 360 + 1
  local x, y, z = 0, 0, 0
  local scaled_constant = 1.4388e7 / temp
  for wavelength = 360, 830 do
    local factor = 1 / (wavelength^5 * (exp(scaled_constant / wavelength) - 1))
    local entry = table[wavelength - 359].value
    x = x + entry[1] * factor
    y = y + entry[2] * factor
    z = z + entry[3] * factor
  end
  local xyz = x + y + z
  return x / xyz, y / xyz, z / xyz
end

local function xy2uv(x, y)
  -- local divisor = x + 15*y + 3
  -- return 4*x / divisor --[[u]], 6*y / divisor --[[v]] 
  local divisor = -2*x + 12*y + 3
  return 4*x / divisor --[[u']], 9*y / divisor --[[v']] 
end

local colorspaces = setmetatable({
  Adobe = {
    xy2RGB = function(x, y, z)
      return 2.0413690 * x + -0.5649464 * y + -0.3446944 * z,
            -0.9692660 * x +  1.8760108 * y +  0.0415560 * z,
             0.0134474 * x + -0.1183897 * y +  1.0154096 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.6400 def /yR 0.3300 def
      /xG 0.2100 def /yG 0.7150 def
      /xB 0.1500 def /yB 0.0600 def
      D65
    --]]
  },
  CIE = {
    xy2RGB = function(x, y, z)
      return 2.3706743 * x + -0.9000405 * y + -0.4706338 * z,
            -0.5138850 * x +  1.4253036 * y +  0.0885814 * z,
             0.0052982 * x + -0.0146949 * y +  1.0093968 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.7355 def /yR 0.2645 def
      /xG 0.2658 def /yG 0.7243 def
      /xB 0.1669 def /yB 0.0085 def
      E_
    --]]
  },
  SMPTE = {
    xy2RGB = function(x, y, z)
      return 3.5053960 * x + -1.7394894 * y + -0.5439640 * z,
            -1.0690722 * x +  1.9778245 * y +  0.0351722 * z,
             0.0563200 * x + -0.1970226 * y +  1.0502026 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.6300 def /yR 0.3400 def
      /xG 0.3100 def /yG 0.5950 def
      /xB 0.1550 def /yB 0.0700 def
      D65
    --]]
  },
  NTSC = {
    xy2RGB = function(x, y, z)
      return 1.9099961 * x + -0.5324542 * y + -0.2882091 * z,
            -0.9846663 * x +  1.9991710 * y + -0.0283082 * z,
             0.0583056 * x + -0.1183781 * y +  0.8975535 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.6700 def /yR 0.3300 def
      /xG 0.2100 def /yG 0.7100 def
      /xB 0.1400 def /yB 0.0800 def
      C_
    --]]
  },
  sRGB = {
    xy2RGB = function(x, y, z)
      local r =  3.2404542 * x + -1.5371385 * y + -0.4985314 * z
      local g = -0.9692660 * x +  1.8760108 * y +  0.0415560 * z
      local b =  0.0556434 * x + -0.2040259 * y +  1.0572252 * z
      if r <= 0.00304 then r = r * 12.92 else r = 1.055 * r^(1/2.4) - 0.055 end
      if g <= 0.00304 then g = g * 12.92 else g = 1.055 * g^(1/2.4) - 0.055 end
      if b <= 0.00304 then b = b * 12.92 else b = 1.055 * b^(1/2.4) - 0.055 end
      return r, g, b
    end,
    GAM = 1,
    --[[
    /primaryIlluminants  {
      return
      /xR 0.6400 def /yR 0.3300 def
      /xG 0.3000 def /yG 0.6000 def
      /xB 0.1500 def /yB 0.0600 def
      D65
    } def
    ]]
  },
  ['Pal-Secam'] = {
    xy2RGB = function(x, y, z)
      return 3.0628971 * x + -1.3931791 * y + -0.4757517 * z,
            -0.9692660 * x +  1.8760108 * y +  0.0415560 * z,
             0.0678775 * x + -0.2288548 * y +  1.0693490 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.6400 def /yR 0.3300 def
      /xG 0.2900 def /yG 0.6000 def
      /xB 0.1500 def /yB 0.0600 def
      D65
    } def
    --]]
  },
  ProPhoto = {
    xy2RGB = function(x, y, z)
      return 1.3459433 * x + -0.2556075 * y + -0.0511118 * z,
            -0.5445989 * x +  1.5081673 * y +  0.0205351 * z,
             0.0000000 * x +  0.0000000 * y +  1.2118128 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.7347 def /yR 0.2653 def
      /xG 0.1596 def /yG 0.8404 def
      /xB 0.0366 def /yB 0.0001 def
      D50
    } def
    --]]
  },
  ColorMatch = {
    xy2RGB = function(x, y, z)
      return 2.6422874 * x + -1.2234270 * y + -0.3930143 * z,
            -1.1119763 * x +  2.0590183 * y +  0.0159614 * z,
             0.0821699 * x + -0.2807254 * y +  1.4559877 * z
    end,
    --[[
    /primaryIlluminants  {
      /xR 0.6300 def /yR 0.3400 def
      /xG 0.2950 def /yG 0.6050 def
      /xB 0.1500 def /yB 0.0750 def
      D50
    } def      
    --]]
  },
}, {__index = function(t, k)
  local target = {}
  exec{kind = 'dict', value = target}
  exec'begin'
  exec(k)
  exec'end'
  table.print({[k] = target})
  local v = {
      --[[
       ["Pal-Secam"]={
  ["primaryIlluminants"]={
   ["kind"]="executable",
   ["value"]={
    ["kind"]="array",
    ["value"]={
     {
      ["kind"]="name",
      ["value"]="xR",
     },
     0.64,
     "def",
     {
      ["kind"]="name",
      ["value"]="yR",
     },
     0.33,
     "def",
     {
      ["kind"]="name",
      ["value"]="xG",
     },
     0.29,
     "def",
     {
      ["kind"]="name",
      ["value"]="yG",
     },
     0.6,
     "def",
     {
      ["kind"]="name",
      ["value"]="xB",
     },
     0.15,
     "def",
     {
      ["kind"]="name",
      ["value"]="yB",
     },
     0.06,
     "def",
     "D65",
    },
   },
  },
  --]]
  --[[
  ["xy2RGB"]={
   ["kind"]="executable",
   ["value"]={
    ["kind"]="array",
    ["value"]={
     {
      ["kind"]="name",
      ["value"]="R",
     },
     3.0628971,
     "X",
     "mul",
     -1.3931791,
     "Y",
     "mul",
     "add",
     -0.4757517,
     "Z",
     "mul",
     "add",
     "def",
     {
      ["kind"]="name",
      ["value"]="G",
     },
     -0.969266,
     "X",
     "mul",
     1.8760108,
     "Y",
     "mul",
     "add",
     0.041556,
     "Z",
     "mul",
     "add",
     "def",
     {
      ["kind"]="name",
      ["value"]="B",
     },
     0.0678775,
     "X",
     "mul",
     -0.2288548,
     "Y",
     "mul",
     "add",
     1.069349,
     "Z",
     "mul",
     "add",
     "def",
    },
   },
  --]]
    xy2RGB = function(x, y, z)
      push{kind = 'name', value = 'X'}
      push(x)
      exec'def'
      push{kind = 'name', value = 'Y'}
      push(y)
      exec'def'
      push{kind = 'name', value = 'Z'}
      push(z)
      exec'def'
      exec(target.xy2RGB)
      exec'R'
      local r = pop_num()
      exec'G'
      local g = pop_num()
      exec'B'
      local b = pop_num()
      return r, g, b
    end,
  }
  t[k] = v
  return v
end})

local function normalisation(r, g, b)
  local maxRGB = max(r, g, b)
  r = r / maxRGB
  g = g / maxRGB
  b = b / maxRGB
  if r < 0 then r = 0 elseif r > 1 then r = 1 end
  if g < 0 then g = 0 elseif g > 1 then g = 1 end
  if b < 0 then b = 0 elseif b > 1 then b = 1 end
  return r, g, b
end

local function gamut(stepXY, GAM, contrast, chromaticityCoordinates, colorspace)
  local space = colorspaces[colorspace]
  GAM = space.GAM or GAM
  local result = {}
  local steps = 1 // stepXY
  -- newpath
  for xPos = 0, steps do
    local x = xPos * stepXY
    for yPos = 0, steps do
      local y = yPos * stepXY
      local z = 1 - x - y
      --[[ This block seems weird, I don't thing that it does what it's supposed to.
      if chromaticityCoordinates ~= 'xy' then
        local u, v = xy2uv(x, y)
        xPos = u * cieUnit
        yPos = v * cieUnit
      end
      ]]
      local r, g, b = normalisation(space.xy2RGB(x, y, z))
      result[yPos * (steps + 1) + xPos + 1] = {kind = 'array', value = {r^GAM * contrast, g^GAM * contrast, b^GAM * contrast}}
    end
  end
  return result, steps + 1, steps + 1
end

return {
  ['.BLKBOD'] = function()
    local tablename = pop_array().value
    local T = pop_num()
    local X, Y, Z = BLKBOD(T, tablename)
    push(X)
    push(Y)
    push(Z)
  end,
  ['.gamut'] = function()
    local colorspace = pop_string().value
    local chromaticityCoordinates = pop_string().value
    local contrast = pop_num()
    local GAM = pop_num()
    local stepXY = pop_num()
    local result, cols, rows = gamut(stepXY, GAM, contrast, chromaticityCoordinates, colorspace)
    push{kind = 'array', value = result}
    push(cols)
    push(rows)
  end,
}, 0
