#!/bin/bash

view() {
    index=$(tail -n1)
    video_info=$(jq -r ".[$index] | tojson" test.json)
    link=$(echo $video_info | jq -r ".video_link")
    jq -n "{watch_time: now, video_info: $video_info}" >> watch.log
    echo "Opening $link in mpv ..."
    mpv "$link"
}

save_to_queue() {
    rg '^\d+$' |
        (while read index; do
            jq -r ".[$index] | tojson" test.json >> queue.log
        done)
}

delete_from_queue() {
    cat | rg 'https' |
        (while read link; do
            # link=$(jq -r ".[$index].video_link" test.json)
            echo $link
            inplace -w queue.log jq "select(.video_link != \"$link\")"
        done)
}

preview() {
    head -n-1
    echo $FZF_PREVIEW_LINES
    echo $FZF_PREVIEW_COLUMNS
}

case $1 in
    view) view; exit ;;
    save) save_to_queue; exit ;;
    preview) preview; exit ;;
    delete) delete_from_queue; exit ;;
esac

ytv_cmd="$0"
fzf_binds=$(cat <<EOF | sd "\n" ""
enter:execute(cat {f} | $ytv_cmd view),
ctrl-w:execute(cat {+f} | $ytv_cmd save),
ctrl-q:reload(jq -srf preproc.jq queue.log),
ctrl-d:execute(cat {f} | $ytv_cmd delete)
EOF
)

jq -rf preproc.jq test.json | fzf --multi --read0 --with-nth=1 -d"\n" --bind "$fzf_binds" --preview "cat {f} | $ytv_cmd preview"
