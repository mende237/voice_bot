
var btn_add = document.getElementById("btn-add");
choises = "<option value=\"id_feature_in_db\"> name of feature 1 for leaf</option><option value=\"id_feature_in_db\"> name of feature 2 for leaf</option>"
var idmax = 0;
var features = document.getElementById("features");

function add_feature(num_seq) {
    feature = document.createElement("div");
    feature.setAttribute("class", "feature");
    feature.setAttribute("id", "feature_" + num_seq);

    /*
    escap = document.createElement("span");
    if(idmax > 0){
        escap.innerHTML ="";
    }*/

    select_feature = document.createElement("select");
    select_feature.setAttribute("name", "feature_" + num_seq);
    select_feature.setAttribute("class", "form-select form-select-sm");
    select_feature.innerHTML = choises;

    btn_delete = document.createElement("a");
    btn_delete.setAttribute("btn_delete_num", num_seq);
    btn_delete.setAttribute("class", "btn btn-primary");
    btn_delete.innerHTML = 'x';

    /*feature.appendChild(escap);*/
    feature.appendChild(select_feature);
    feature.appendChild(btn_delete);
    features.appendChild(feature);

    idmax++;
    btn_delete.addEventListener('click', (e) => {
        num = parseInt(e.currentTarget.getAttribute("btn_delete_num"));
        features.removeChild(document.getElementById("feature_" + num));
        for (i = num + 1; i < idmax; i++) {
            feature_ = document.getElementById("feature_" + i);
            feature_.childNodes[0].setAttribute("name", "feature_" + (i - 1));
            feature_.childNodes[1].setAttribute("btn_delete_num", (i - 1));
            feature_.setAttribute("id", "feature_" + (i - 1));
        }
        idmax--;
    });
}

btn_add.addEventListener('click', () => {
    add_feature(idmax);
});