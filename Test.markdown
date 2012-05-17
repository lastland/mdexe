This docunment is only for test.

include 'Test-Content.markdown'

Exec:

    echo 'exec test succeed!'

Append_to 'Test.file' :

    append test succeed!

Replace_in 'Test.file' :

    should be replaced if the replace test succeeded

to :

    has been replaced

End.
