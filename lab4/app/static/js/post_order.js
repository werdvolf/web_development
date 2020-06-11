function  make_order()
{
    let data = {
        "company_name": document.getElementById('company_name').value,
        "min_budget": document.getElementById('min_budget').value,
        "max_budget": document.getElementById('max_budget').value,
        "media": check("media_input"),
        "outdoor": check("outdoor_input"),
        "product_placement": check("product_placement_input"),
        "tv": check("tv_input"),
        "radio":check("radio_input"),
        "description": document.getElementById('description_input').value
    };

    loader.call('get', 'order/make_order', data)
        .then(
            resolve => { console.log(resolve); },
            reject => console.error(data)
        );
}

function check(id) {
  var x = document.getElementById(id).checked;
  if (x == false) {
      return 0;
  }
  else {
      return 1;
  }

}

