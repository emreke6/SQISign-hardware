set fp [open "src/modmul.v" r]
set data [read $fp]
close $fp

set lines [split $data "\n"]
set line_no 1

foreach line $lines {
    puts "[format "%4d" $line_no]: $line"
    incr line_no
}
