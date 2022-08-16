function zebraTables()
{
  $("table tr:even").addClass("even");
  $("table tr:odd").addClass("odd");
}

function loadContent( theUrl )
{
  uiBlock();
  $("#main-content").load( theUrl ,"",uiUnblock);
}

function loadSummaryTable(theId)
{
  uiBlock();
  $("#main-content").load("/sensorSummaryTable/" + theId + "/","",uiUnblock);
}

function uiBlock() {
    $.blockUI({
        message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
        css: {
            border: '1px solid #000',
            background: 'rgba(0, 0, 0, 0.3)',
            width: '550px',
            height:'550px'
        }
    });
}

function uiUnblock() {
    $.unblockUI();
}

function setupPreviewDialogCart( )
{
  $('#main-content').on('click','.mini-icon', function () {
    var myRecordId = $(this).attr('longdesc');
    $('#modalContainer').load("/thumbnailpage/" + myRecordId + "/");
    $('#myModal').modal('show');
  });
}

function removeFromCart(theId, theObject)
{
  uiBlock();
  //check if this product has delivery details form
  var myOrderForm_refs = $('#add_form #id_ref_id');
    if (myOrderForm_refs.length >0){
      var current_refs=myOrderForm_refs.val();
      //check if current_refs are empty, and convert to array
      if (current_refs.length){
          current_refs=current_refs.split(',');
      } else {
          current_refs=[];
      }
      //get removed ref_id
      var ref_id=theObject.parent().parent().find('a.show_form').attr('ref_id')
      var index = current_refs.indexOf(ref_id);
      if (index>-1){
          current_refs.splice(index,1);
          myOrderForm_refs.val(current_refs.join(','));
      }
    }
  $.get("/removefromcart/" + theId + "/?xhr")
    .done(function () {
      theObject.parent().parent().remove();
      //-1 for the header row
      var myRowCount = $("#cart-contents-table tr").length - 1;
      if ((myRowCount < 1) && ($("#id_processing_level").length != 0))
      {
        //second clause above to prevent this action when minicart is being interacted with
        window.location.replace("/emptyCartHelp/");
      }
      // remove feature from layer
      if (typeof cartLayer != 'undefined')
        cartLayer.removeFeature(theId);
    })
    .fail(function () {
      alert('Gnomes.. again!');
    });
  uiUnblock();
  return false;
}

function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }