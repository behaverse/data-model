-- Renders a quiet status badge under the title for pages with `status:` front matter.
-- Values: draft | open-design-area
local LABELS = {
  ["draft"] = "Draft — content still being designed",
  ["open-design-area"] = "Open design area — direction not yet settled",
}

function Pandoc(doc)
  local status = doc.meta.status
  if status == nil then return doc end
  local key = pandoc.utils.stringify(status)
  local label = LABELS[key]
  if label == nil then return doc end
  local badge = pandoc.Div(
    { pandoc.Plain({ pandoc.Str(label) }) },
    pandoc.Attr("", { "status-badge", "status-" .. key })
  )
  table.insert(doc.blocks, 1, badge)
  return doc
end
