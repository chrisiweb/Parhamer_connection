---- luapstricks-plugin-pstsolides3d.lua
-- Copyright 2021--2023 Marcel Krüger <tex@2krueger.de>
-- Converted from PostScript in pst-solides3d.pro
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

--[[
-- Solides are represented as four element arrays containing:
-- {
--   Sommets, Faces, Colors_Faces, InOut_Table
-- }
--]]

local function issolid(candidate)
  if type(candidate) ~= 'table' then return false end
  local kind = candidate.kind
  if kind == 'executable' then return issolid(candidate.value) end
  if kind ~= 'array' then return false end
  candidate = candidate.value
  if #candidate ~= 4 then return false end

  local sommets = candidate[1]
  if type(sommets) ~= 'table' then return false end
  if sommets.kind == 'executable' then
    sommets = sommets.value
    if type(sommets) ~= 'table' then return false end
  end
  if sommets.kind ~= 'array' then return false end

  local faces = candidate[2]
  if type(faces) ~= 'table' then return false end
  if faces.kind == 'executable' then
    faces = faces.value
    if type(faces) ~= 'table' then return false end
  end
  if faces.kind ~= 'array' then return false end

  local faceColors = candidate[3]
  if type(faceColors) ~= 'table' then return false end
  if faceColors.kind == 'executable' then
    faceColors = faceColors.value
    if type(faceColors) ~= 'table' then return false end
  end
  if faceColors.kind ~= 'array' then return false end

  local IO = candidate[4]
  if type(IO) ~= 'table' then return false end
  if IO.kind == 'executable' then
    IO = IO.value
    if type(IO) ~= 'table' then return false end
  end
  if IO.kind ~= 'array' then return false end
  IO = IO.value
  if #IO ~= 4 then return false end

  return type(IO[1]) == 'number' and type(IO[2]) == 'number' and type(IO[3]) == 'number' and type(IO[4]) == 'number'
end

local function nullsolid(candidate)
  assert(issolid(candidate), 'Error type argument dans "nullsolid"')
  return #candidate[1].value == 0
end

local function getp3d(sommets, indices)
  -- TODO
  error'TODO'
end

local function solidgetsommetsface(solid, i)
  assert(issolid(solid), 'Error : mauvais type d argument dans solidgetsommetsface')
  local table_sommets = solid.value[1].value
  local table_faces = solid.value[2].value
  local table_indices = table_faces[i + 1]
  local result = {}
  for j=1, #table_indices do
    result[j] = getp3d(table_sommets, table_indices[j])
  end
  return result
end

local function isobarycentre3d(face)
  -- TODO
  error'TODO'
end

local function solidcentreface(solid, i)
  return isobarycentre3d(solidgetsommetsface(solid, i))
end


local function drawsolid(solid, order, peintrealgorithme)
  if nullsolid(solid) then return end
  local sommets = solid[1].value
  local n = #sommets // 3

  local faces = solid[2].value

  if not order then
    order = {}
    if peintrealgorithme then
      for i = 1, #faces do
        local face = solidcentreface(solid, i-1)
        order[i] = face GetCamPos distance3d
      end
      order = order doublequicksort pop reverse
    else
      for i = 1, #faces do
        order[i] = i - 1
      end
      order = {kind = 'array', value = order}
    end
  end

  0 1 faces length 1 sub {
     /k exch def
     /i order k get def
     gsave
        solid i solidfacevisible? {
           solid i dessinefacevisible
        } if
     grestore
  } for
  aretescachees {
     0 1 F length 1 sub {
        /k exch def
        /i order k get def
        gsave
           solid i solidfacevisible? not {
              solid i dessinefacecachee
           } if 
        grestore
     } for
  } if
end

return {
  drawsolid = function()
    local order
    local solid = pop()
    if not issolid(solid) then
      solid, order = pop(), solid
      assert(issolid(solid), 'Error : mauvais type d argument dans drawsolid')
    end
    return drawsolid(solid, order)
  end,
  issolid = function()
    push(issolid(pop()))
  end,
}, 0
