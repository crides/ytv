to_entries
| sort_by(-(.value.rank.rank))
| map(
    [.key, .value]
    | [(.[1] | ("[" + .channel_name + "] " + .title,
               "Length: " + (.length | tostring),
               "Views: " + (.view_count | tostring),
               "Publish time: " + (.publish_time | tostring),
               "Ranks: ",
               (
                    .rank
                    | to_entries
                    | map("  " + .key + ": " + (.value | tostring))
                    | .[]
               )
               )),
      .[0]]
    | join("\n"))
| join("\u0000")
