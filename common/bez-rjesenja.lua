-- Drops every slide whose title starts with "Рјешење", so students get tasks without answers.
local PREFIX = "Рјешење"

function Pandoc(doc)
  local out, skipping = {}, false
  for _, block in ipairs(doc.blocks) do
    local new_slide = (block.t == "Header" and block.level <= 2) or block.t == "HorizontalRule"
    if new_slide then
      skipping = block.t == "Header" and pandoc.utils.stringify(block):sub(1, #PREFIX) == PREFIX
      -- A "---" left before a dropped slide would become an empty slide.
      if skipping and out[#out] and out[#out].t == "HorizontalRule" then out[#out] = nil end
    end
    if not skipping then out[#out + 1] = block end
  end
  doc.blocks = out
  return doc
end
