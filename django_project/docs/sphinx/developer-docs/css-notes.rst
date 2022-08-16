BOOTSTRAP IMPLEMENTATION
------------------------

We are using a fixed-width container (.container) with fluid rows (.row-fluid).

Although Bootstrap docs suggest using .row within fixed-width containers, we use
.row-fluid in order to fix layout issues with the .well. Wells are not intended
to have grids within them due to the extra padding they introduce, as per this issue:

https://github.com/twitter/bootstrap/issues/1446

However, this problem is solved by using .row-fluid which is acceptable as per this issue:

https://github.com/twitter/bootstrap/issues/2463


