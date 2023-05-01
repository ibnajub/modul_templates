function payFromBalance(obj){
	if(confirm(obj.confirm.value)){
		new _uWnd('win-'+obj.id,obj.rem.value,-340,-120,{autosize:0,modal:1,closeonesc:1,resize:0},{form:obj.id,url:obj.action});
	}else{
		if(typeof window.shop_redirect != 'undefined'){
			location.href = window.shop_redirect;
			window.shop_redirect = null;
		}
	}
	return false;
}

function shopSelectPeriod(obj){
	var tmp = obj.options[obj.selectedIndex].value.split('|');
	var prefix = ( (obj.id=='scdate') ? 'c' : '' );
	$('#'+prefix+'date1').val(tmp[0]);
	$('#'+prefix+'date2').val(tmp[1]);
}

function getDigitalGoods(i){
	if(digital_goods[i][0] == 1)
		location.href = digital_goods[i][2];
	else if(digital_goods[i][0] == 2)
		new _uWnd('getDigitalGoods'+i, digital_goods[i][1], 350, 60, {autosize:1, closeonesc:1, align:'center', icon:'/.s/img/icon/fm.png'}, digital_goods[i][2]);

	return false;
}

function price2Basket() {
	if (_shopLockButtons()) return false;
	_uPostForm('', {
			type: 'POST',
			data: $('#shop-price-form').serializeArray().filter(function (item) {
				var res = 0;
				var id = item['name'].split('_');
				if (id[0] == 'oval') {
					var item_elem = $('#shop-price-form [name=cnt_' + id[1] + ']');
					if (item_elem.attr('type') == 'checkbox') {
						res = ( item_elem.attr("checked") ? 1 : 0);
					} else {
						res = ( item_elem.val() > 0 ? 1 : 0);
					}
				} else {
					res = item['value'] != 0;
				}
				return res;
			}),
			url: '/shop/basket'
		}
	);
	$('input.pinput').attr('disabled', 'disabled');
	return false;
}

function hideGoods(id, ssid, pref){
	if(_shopLockButtons()) return false;
	$('#'+pref+'-hib'+id).attr('src', '/.s/img/fr/EmnAjax.gif');
	_uPostForm('',{type:'POST',url:'/shop/' + id + '/edit',data:{'mode':'edit', 'method':'hide', 'id':id, 'pref':pref, 'ssid':ssid}});
	return false;
}

function upGoods(id, ssid, pref){
	if(_shopLockButtons()) return false;
	$('#'+pref+'-qub'+id).attr('src', '/.s/img/fr/EmnAjax.gif');
	_uPostForm('',{type:'POST',url:'/shop/' + id + '/edit',data:{'mode':'edit', 'method':'quickup', 'id':id, 'pref':pref, 'ssid':ssid}});
	return false;
}

function deleteGoods(id, ssid, pref){
	if(_shopLockButtons()) return false;
	$('#'+pref+'-dib'+id).attr('src', '/.s/img/fr/EmnAjax.gif');
	_uPostForm('',{type:'POST',url:'/shop/' + id + '/edit',data:{'mode':'edit', 'method':'delete', 'id':id, 'pref':pref, 'ssid':ssid}});
	return false;
}

function shopCatBlocks(obj, cname, c1, c2){
	var id = -1;
	var ti = 0;
	var hb = $('.cat-blocks ul:visible');
	if(hb.length){
		ti = $(hb).prev().attr('id').split('blocks-rt-')[1];
	}
	if(obj !== undefined){
		id = $(obj).attr('id').split('blocks-rt-')[1];
		//скрываем отображенный блок подкатегорий
		if(hb.length){
			$(hb).animate({height:'hide'}, 200).prev().addClass(c1).removeClass(c2);
		}
		//показываем, если скрыт нужный блок подкатегорий
		if(ti != id ){
			$('#blocks-ch-'+id).animate({height:'show'}, 200);
			$('#blocks-rt-'+id).removeClass(c1).addClass(c2);
		}
	}

	var page = parseInt($('#cid-p-0').val());
	var cval = '0=1|'+page;
	$('.cid-p').each(function(){
		var el_id = $(this).attr('id').replace('cid-p-', '')
		page = $(this).val();

		if((el_id == id && ti != id) || (obj == undefined && el_id == ti)){
			cval += ','+el_id+'=1|'+page;
		}else{
			if(page > 1){
				cval += ','+el_id+'=0|'+page;
			}
		}
	});

	uSetCookie(cname, cval, 3600*24*30, '/');
}

function shopCatExpand(obj, cname){
	$(obj).toggleClass('plus').toggleClass('minus').parent().children('ul').toggle();
	return _shopTreeStore(cname);
}

function categoryFilter(field, val, fromURL){
	if(_shopLockButtons()) return false;

	var res = decodeURIComponent(document.location.href);

	if(!fromURL){
		_shopFadeControl('goods_cont');
		res = res.replace(/\;(?:[0-9]+)/, '');
		//_uPostForm('',{type:'POST',url:location.href,data:{'mode':'filter', 'field':field, 'value':(field != 'f_status' ? shop_filter_vals[val] : val)}});
		_uPostForm('', {type:'POST', url:res, data:{'mode':'filter', 'field':field, 'value':shop_filter_vals[val]}});
	}else{
		if(field == 'f_status') {
			res = res.replace(/\;f_status\=[0-9]/g, '');
			res += (val ? ';f_status='+val : '');

		}else{
			var reg = new RegExp("\;f\_"+field+"=(?:[0-9a-zA-Z-_]+)?", "g");
			res = res.replace(reg, '');
			res += (shop_filter_vals[val] ? ';f_'+field+'='+encodeURIComponent(shop_filter_vals[val]) : '');
		}

		res = res.replace(/\;(?:[0-9]+)/, '');

		var res2 = /(all|wishlist)(?:\/?(.*))?$/.exec(res);
		if (res2 && (res2[1] && (res2[1] == 'all' || res2[1] == 'wishlist')) && res2[2]) {
			var fVal = /(?:(\;.*))/.exec(res2[2]);
			if (fVal && fVal[1]) {
				var reg = new RegExp('/' + res2[2] + '$', 'g');
				res = res.replace(reg, fVal[1]);
			}
		}else{
			res2 = /user(?:\/+([0-9]+)(?:\/+(goods)(?:\/?(.*))?)?)?$/.exec(res);
			if (res2 && res2[3]) {
				var fVal = /(?:(\;.*))/.exec(res2[3]);
				if (fVal && fVal[1]) {
					var reg = new RegExp('/' + res2[3] + '$', 'g');
					res = res.replace(reg, fVal[1]);
				}
			}
		}

		document.location.href = res;
	}

	return false;
}

var shop_page;
var shop_num_pages;
function shopPageMore(data){
	if(_shopLockButtons()) return false;
	$('#shop-page-more').addClass('wait').show();
	$('.shop-more-scroll').addClass('gTableTop');
	_uPostForm('', {type:'POST', url:decodeURIComponent(document.location.href), data:data});
	return false;
}

function shopPageScrollClose(obj){
	$(obj).parent().removeClass('gTableTop');
	return false;
}

function categorySort(colum, order){
	if(_shopLockButtons()) return false;
	_shopFadeControl('goods_cont');
	_uPostForm('', {type:'POST', url:decodeURIComponent(document.location.href), data:{'mode':'sort', 'sort':colum, 'order':order}});
	return false;
}

function _shopTreeStore(cname){
	var cval = '0=0|';
	var p0 = $('#cid-p-0');
	if(p0.length > 0){
		cval += $('#cid-p-0').val();
	}else{
		cval += '1';
	}
	$('li ul.cat-tree:visible').each(function(){
		var cat_id = $(this).parent().attr('id').split('cid-')[1];
		var page = $(this).parent().find('#cid-p-'+cat_id).val();
		cval += ',' + cat_id + '=1|'+page;
	});

	uSetCookie(cname, cval, 3600*24*30, '/');

	return false;
}

var lock_categories = 0;
/*
получение набора категорий
pid - id родительской категории, для которой нужно получить набор
cname - кука с которой нужно взять список раскрытых категорий
el_id - id элемента в DOM-дереве, после которого нужно вставить полученный набор
el_more - елемент ссылка "Показать еще"
*/
function shopCatShowMore(pid, ssid, cname, el_id, el_more, sh_g){
	if(lock_categories == 1){
		return false;
	}

	lock_categories = 1;

	var pageEl = $('#cid-p-'+pid);
	pageEl.val(parseInt(pageEl.val())+1);

	if(el_id.search(/blocks-rt-/) != -1 || el_id.search(/blocks-ch-/) != -1){
		shopCatBlocks(undefined, cname, '', '');
	}else{
		_shopTreeStore(cname);
	}

	el_more.html($('<div class="myWinLoad" style="margin:5px; height: 31px !important;"></div>'));

	_uPostForm(
		'',
		{
			type:'POST',
			url:'/shop/catalog',
			data:{
				cat_pid: pid,
				el_id: el_id,
				mode: 'cat_subblock',
				cname: cname,
				sh_g: sh_g,
				ssid: ssid
			}
		}
	);

	$(el_more).addClass('need_remove');
}

var lock_cats_catalog = 0;
function shopCatsCatalogShowMore(colums, childs, show_goods_count, parent, ssid, el_more) {
	if (lock_cats_catalog == 1) {
		return false;
	}

	lock_cats_catalog = 1;

	var pageEl = $('#cats_catalog_cid-p-0');
	pageEl.val(parseInt(pageEl.val()) + 1);

	el_more.html($('<div class="myWinLoad" style="margin:5px; height: 31px !important;"></div>'));

	_uPostForm(
		'',
		{
			type: 'POST',
			url: '/shop/catalog',
			data: {
				colums: colums,
				childs: childs,
				show_goods_count: show_goods_count,
				parent: parent,
				page: pageEl.val(),
				mode: 'cats_catalog_subblock',
				ssid: ssid
			}
		}
	);

	$("#show_cats_more_block").parent().addClass('show_cats_more_block_need_remove');
}

var lock_buttons = 0;
function _shopLockButtons(){

	if(lock_buttons) return true;

	lock_buttons = 1;

	return false;
}

function _dynform(values, url){

	if(url==undefined) url = '';

	var fd = '';
	for(i in values){
		fd += '<input type="hidden" name="'+i+'" value="'+values[i]+'">';
	}
	var obj = $('#dyn-post');
	if(obj.length){
		$(obj).html(fd).attr('action', url);

	}else{
		$('body').append('<form id="dyn-post" action="'+url+'" method="post">'+fd+'</form>');
	}
}

function uSetCookie (name,value,expir,path,domain,secure) {
	var today = new Date();
	var expires = new Date();
	expires.setTime(today.getTime() + 1000*expir);

	document.cookie = name + "=" + escape (value) +
	((expires) ? "; expires=" + expires.toGMTString() : "") +
	((path) ? "; path=" + path : "/") +
	((domain) ? "; domain=" + domain : "") +
	((secure) ? "; secure" : "");
}

function editOrderFieldCancel(oid, fid, value) {
	$('.o'+oid+'-field-value-'+fid+'-wrapper').html(value);
	lock_buttons=0;
	curr_send = false;
}

function editOrderField(oid, field_id, field_name, field_type, field_values_list, field_value, update) {
	for(key in _uWnd.all){
		if(_uWnd.all[key] != null && _uWnd.all[key].name.search(/inv\_wnd\_(.+)/)!=-1) inv_wnd_opened = true;
	}
	if(inv_wnd_opened && update!='popup') return;
	if(_shopLockButtons() || curr_send) return;
	var inv_wnd_opened = false;

	curr_send = oid+'_'+field_id;
	switch(field_type) {
		case 'phone':
		case 'email':
		case 'text':
		case 'textarea':
		case 'promo':
		case 'gmaps':
			new _uWnd(
				'wnd_'+field_id,
				field_name,
				550,
				350,
				{
					autosize:1,
					resize:0,
					modal:0,
					closeonesc:1,
					icon:'/.s/img/icon/pent.png',
					onclose:function(){lock_buttons=0; curr_send=false;}
				},
				{
					url:'/shop/checkout',
					type:'POST',
					data:{
						'id':oid,
						'mode':'inv_chfld',
						'fid':field_id,
						'ftype':field_type,
						'fval':field_value,
						'ssid':ssid,
						'update':update
					},
					cache:1
				}
			);
			break;
		case 'checkbox':
			editOrderFieldSend(oid, field_id, field_value, update);
			break;
		case 'radio':
		case 'select':
			_uPostForm('', {url:'/shop/checkout', type:'POST', data:{
				mode:'inv_chfld',
				id:oid,
				fid:field_id,
				ftype:field_type,
				update:update,
				ssid:ssid
			}});
			var load_img = '/img/sh/wait.gif';
			if(update == 'order') load_img = '/img/ma/m/i3.gif';
			$('.o'+oid+'-field-value-'+field_id+'-wrapper')
				.attr('old_val', $('.'+oid+'-field-value-'+field_id+'-wrapper').html())
				.html('<img alt="" id="inote-'+oid+'-wait" src="/.s'+load_img+'">');
			break;
		default:
			//console.log("DEFAULT IN AJAX");
			curr_send = false;
			lock_buttons = 0;
			break;
	};
	return false;
};

function editOrderFieldSend(id, field_id, field_value, update) {
	//if(curr_send != id+'_'+field_id){
		//_uButtonEn('inote-form-'+id,1);
	//}else{
		var formid = (field_value !== undefined ? '' : 'order-field-'+field_id);
		if( update == 'order' )
			$('.o'+id+'-field-value-'+field_id+'-wrapper')
				.hide()
				.after('<img alt="" id="inote-'+id+'-wait" src="/.s/img/ma/m/i3.gif">');
		else
			$('.o'+id+'-field-value-'+field_id+'-wrapper')
				.hide()
				.after('<img alt="" id="inote-'+id+'-wait" src="/.s/img/sh/wait.gif">');

		field_value = (field_value ? field_value : document.getElementById('fval').value);

		_uPostForm(formid, {type:'POST', url:'/shop/checkout', data:{
			mode:'inv_chfld_save',
			update:update,
			id:id,
			fid:field_id,
			fval:field_value,
			ssid:ssid
		}});
		_uWnd.close('wnd_'+field_id);
		curr_send = false;
	//}
	return false;
}

// Maps
function create_map(id, type, lat, lng, z){
	if(type == undefined || type == '' || type == null){
		plog('Type of maps undefined', 'MAPS');
		return false;
	};
	$('#'+id+'-canvas').attr('style', 'height:450px;overflow:hidden;').next('div').removeAttr('style');
	switch(type){
		case 'gmap': create_gmap(id, lat, lng, z);break;
		case 'ymap': create_ymap(id, lat, lng, z);break;
	}
	return 1;
}

function create_gmap(id, lat, lng, z){
	plog('GMAP START', 'MAPS');

	var myOptions = {
	   zoom: parseInt(z),
	   mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	gmaps[id].map = new google.maps.Map(document.getElementById(id+'-canvas'), myOptions);


	if(gmaps[id].options == undefined) gmaps[id].options = {};
	if(gmaps[id].options.is_editable == undefined) gmaps[id].options.is_editable = false;
	if(gmaps[id].options.placemarks == undefined){
		gmaps[id].latlng = new google.maps.LatLng(lat, lng);
		gmaps[id].placemark = new google.maps.Marker({
			position: gmaps[id].latlng,
			map: gmaps[id].map,
			draggable: gmaps[id].options.is_editable ? true : false
		});
		gmaps[id].map.setCenter(gmaps[id].latlng);
		gmaps[id].placemark.inner_id = id;
		if(gmaps[id].options.is_editable) {
			google.maps.event.addListener(gmaps[id].placemark, 'dragstart', function() {
				if(gmaps[this.inner_id].placemark_info != undefined)
				gmaps[this.inner_id].placemark_info.close();
			});
			google.maps.event.addListener(gmaps[id].placemark, 'dragend', function() {
				gmap_set_data(this.inner_id);
				gmap_get_address(this.inner_id);
			});
		}
		gmap_get_address(id);
		google.maps.event.addListener(gmaps[id].placemark, 'click', function() {
			gmaps[this.inner_id].placemark_info = new google.maps.InfoWindow({content:$('#'+this.inner_id+'-addr').val()});
			gmaps[this.inner_id].placemark_info.open(gmaps[this.inner_id].map, gmaps[this.inner_id].placemark);
		});

	}else{
		gmaps[id].placemarks = {};
		gmaps[id].geopoints = [];
		gmaps[id].bounds = new google.maps.LatLngBounds();
		for(key in gmaps[id].options.placemarks){
			var point = new google.maps.LatLng(gmaps[id].options.placemarks[key].lat, gmaps[id].options.placemarks[key].lng);
			gmaps[id].bounds.extend(point);
			gmaps[id].geopoints.push(point);
			gmaps[id].placemarks[key] = new google.maps.Marker({
				position: point,
				map: gmaps[id].map
			});
			gmaps[id].placemarks[key].inner_key = key;
			gmaps[id].placemarks[key].inner_id = id;
			google.maps.event.addListener(gmaps[id].placemarks[key], 'click', function() {
				gmaps[this.inner_id].placemarks[this.inner_key].description = new google.maps.InfoWindow({content:gmaps[this.inner_id].options.placemarks[this.inner_key].balloon});
				gmaps[this.inner_id].placemarks[this.inner_key].description.open(gmaps[this.inner_id].map, gmaps[this.inner_id].placemarks[this.inner_key]);
			});
		};
		gmaps[id].rect = new google.maps.Rectangle({
			map:gmaps[id].map,
			bounds:gmaps[id].bounds,
			strokeColor: "#FF0000",
			strokeOpacity: 0.8,
			strokeWeight: 3,
			fillColor: "#FF0000",
			fillOpacity: 0.35
		});
		//gmaps[id].map.setCenter(gmaps[id].bounds.getCenter());
		gmaps[id].map.fitBounds(gmaps[id].bounds);

	}
}

function gmap_set_data(id) {
	$('#'+id+'-lat').val(gmaps[id].placemark.getPosition().lat());
	$('#'+id+'-lng').val(gmaps[id].placemark.getPosition().lng());
}

function gmap_get_address(id) {
	var geocoder = new google.maps.Geocoder();
	var latlng = gmaps[id].placemark.getPosition();
	geocoder.geocode({'latLng': latlng}, function (results, status) {
		if (status != google.maps.GeocoderStatus.OK && (results[1] == undefined || results[1] == null)) {
			_uWnd.alert("Error while geolocating. Status Code:" + status);
		} else {
			gmaps[id].map_addr = results[1].formatted_address;
			$('#'+id+'-addr').val(results[1].formatted_address).trigger('onchange');;
		}
	});
}

function create_ymap(id, lat, lng, z){
	plog('YANDEXMAP START', 'MAPS');
	YMaps.jQuery(function () {
        ymaps[id].map = new YMaps.Map(YMaps.jQuery("#"+id+"-canvas")[0]);
		ymaps[id].map.enableScrollZoom();
		ymaps[id].map.addControl(new YMaps.TypeControl());
		ymaps[id].map.addControl(new YMaps.ToolBar());
		ymaps[id].map.addControl(new YMaps.Zoom());
		ymaps[id].map.addControl(new YMaps.MiniMap());
		ymaps[id].map.addControl(new YMaps.ScaleLine());
		if(ymaps[id].options == undefined) ymaps[id].options = {};
		if(ymaps[id].options.is_editable == undefined) ymaps[id].options.is_editable = false;
		if(ymaps[id].options.placemarks == undefined){
			ymaps[id].geopoint = new YMaps.GeoPoint(lng, lat);
			ymaps[id].map.setCenter(ymaps[id].geopoint, z);
			ymaps[id].placemark = new YMaps.Placemark(ymaps[id].geopoint, {draggable: ymaps[id].options.is_editable});
			if(ymaps[id].options.is_editable){
				YMaps.Events.observe(
					ymaps[id].placemark,
					ymaps[id].placemark.Events.DragEnd,
					function (placemark) {
						ymap_get_adress(id);
						ymap_set_data(id);
					}
				);
			}
			ymap_get_adress(id);
			ymaps[id].map.addOverlay(ymaps[id].placemark);
		}else{
			ymaps[id].placemarks = {};
			ymaps[id].geopoints = [];
			for(key in ymaps[id].options.placemarks){
				var point = new YMaps.GeoPoint(ymaps[id].options.placemarks[key].lng, ymaps[id].options.placemarks[key].lat);
				ymaps[id].geopoints.push(point);
				ymaps[id].placemarks[key] = new YMaps.Placemark(point);
				ymaps[id].placemarks[key].description = ymaps[id].options.placemarks[key].balloon;
				ymaps[id].map.addOverlay(ymaps[id].placemarks[key]);
			};
			bounds = new YMaps.GeoCollectionBounds(ymaps[id].geopoints);
			var style = new YMaps.Style();
			style.polygonStyle = new YMaps.PolygonStyle();
			style.polygonStyle.fill = 1;
			style.polygonStyle.outline = 1;
			style.polygonStyle.strokeWidth = 10;
			style.polygonStyle.strokeColor = "ffff0088";
			style.polygonStyle.fillColor = "ff000055";
			var polygon = new YMaps.Polygon([bounds.getLeftTop(), bounds.getRightTop(), bounds.getRightBottom(), bounds.getLeftBottom()], {style:style});
			ymaps[id].map.setBounds(bounds);
			ymaps[id].map.addOverlay(polygon);
		}

    })
}

function ymap_set_data(id) {
	$('#'+id+'-lat').val(ymaps[id].placemark.getGeoPoint().getY()).trigger('onchange');
	$('#'+id+'-lng').val(ymaps[id].placemark.getGeoPoint().getX()).trigger('onchange');
}

function ymap_get_adress(id) {
	var geocoder = new YMaps.Geocoder(ymaps[id].placemark.getGeoPoint(), {results: 1});
	YMaps.Events.observe(geocoder, geocoder.Events.Load, function () {
		if (this.length()) {
			ymaps[id].placemark.setBalloonContent(this.get(0).text);
			if(ymaps[id].options.is_editable){
				$('#'+id+'-addr').val(this.get(0).text).trigger('onchange');
			}
			return true;
		}else{
			plog('Place not found', 'MAPS-GEOCODER');
			return false;
		}
	});
}

// ImageList

var image_list={
	ajaxloadingmsg: '<div style="background:url(/.s/img/ma/m/i3.gif) no-repeat center bottom; height:50px;" ></div>',
	defaultbuttonsfade:0.3, // fade degree for disabled nav buttons (0=completely transparent, 1=completely opaque)
	configholder: {},

	getCSSValue:function(val){ //Returns either 0 (if val contains 'auto') or val as an integer
		return (val=="auto")? 0 : parseInt(val)
	},

	getoffset:function(what, offsettype){
		return (what.offsetParent)? what[offsettype]+this.getoffset(what.offsetParent, offsettype) : what[offsettype]
	},

	fadebuttons:function(config, currentpanel){
		config.$leftnavbutton.fadeTo('fast', currentpanel==0? this.defaultbuttonsfade : 1)
		config.$rightnavbutton.fadeTo('fast', currentpanel==config.lastvisiblepanel? this.defaultbuttonsfade : 1)
	},

	addnavbuttons:function(config, currentpanel){
		$('#image-lnav').remove();
		$('#image-rnav').remove();
		config.$leftnavbutton=$('<img id="image-lnav" src="'+config.defaultbuttons.leftnav[0]+'">').css({zIndex:50, position:'absolute', left:/* config.offsets.left+ */config.defaultbuttons.leftnav[1]+'px', top:/* config.offsets.top+ */config.defaultbuttons.leftnav[2]+'px', cursor:'hand', cursor:'pointer'}).appendTo('#image-list-cont')
		config.$rightnavbutton=$('<img id="image-rnav" src="'+config.defaultbuttons.rightnav[0]+'">').css({zIndex:50, position:'absolute', right:/* left:config.offsets.left+config.$gallery.get(0).offsetWidth+ */config.defaultbuttons.rightnav[1]+'px', top:/* config.offsets.top+ */config.defaultbuttons.rightnav[2]+'px', cursor:'hand', cursor:'pointer'}).appendTo('#image-list-cont')
		config.$leftnavbutton.on('click', function(){ //assign nav button event handlers
			image_list.stepBy(config.galleryid, -config.defaultbuttons.moveby)
		})
		config.$rightnavbutton.on('click', function(){ //assign nav button event handlers
			image_list.stepBy(config.galleryid, config.defaultbuttons.moveby)
		})
		if (config.panelbehavior.wraparound==false){ //if carousel viewer should stop at first or last panel (instead of wrap back or forth)
			this.fadebuttons(config, currentpanel)
		}
		return config.$leftnavbutton.add(config.$rightnavbutton)
	},

	alignpanels:function(config){
		var paneloffset=0
		config.paneloffsets=[paneloffset] //array to store upper left offset of each panel (1st element=0)
		config.panelwidths=[] //array to store widths of each panel
		config.$panels.each(function(index){ //loop through panels
			var $currentpanel=$(this)
			$currentpanel.css({float: 'none', position: 'absolute', left: paneloffset+'px'}) //position panel
			$currentpanel.on('click', function(e){return config.onpanelclick(e.target)}) //bind onpanelclick() to onclick event
			paneloffset+=image_list.getCSSValue($currentpanel.css('marginRight')) + parseInt($currentpanel.get(0).offsetWidth || $currentpanel.css('width')) //calculate next panel offset
			config.paneloffsets.push(paneloffset) //remember this offset
			config.panelwidths.push(paneloffset-config.paneloffsets[config.paneloffsets.length-2]) //remember panel width
		})
		config.paneloffsets.pop() //delete last offset (redundant)
		var addpanelwidths=0
		var lastpanelindex=config.$panels.length-1
		config.lastvisiblepanel=lastpanelindex
		for (var i=config.$panels.length-1; i>=0; i--){
			addpanelwidths+=(i==lastpanelindex? config.panelwidths[lastpanelindex] : config.paneloffsets[i+1]-config.paneloffsets[i])
			if (config.gallerywidth>addpanelwidths){
				config.lastvisiblepanel=i //calculate index of panel that when in 1st position reveals the very last panel all at once based on gallery width
			}
		}
		//alert(paneloffset+' - '+config.currentpanel);
		config.$belt.css({width: paneloffset+'px'}) //Set Belt DIV to total panels' widths
		config.currentpanel=(typeof config.currentpanel=="number" && config.currentpanel<config.$panels.length)? config.currentpanel : 0
		if (config.currentpanel!=0){
			var endpoint=config.paneloffsets[config.currentpanel]+(config.currentpanel==0? 0 : config.beltoffset)
			config.$belt.css({left: -endpoint+'px'})
		}
		if (config.defaultbuttons.enable==true){ //if enable default back/forth nav buttons
			var $navbuttons=this.addnavbuttons(config, config.currentpanel)
			$(window).on("load resize", function(){ //refresh position of nav buttons when page loads/resizes, in case offsets weren't available document.oncontentload
				config.offsets={left:image_list.getoffset(config.$gallery.get(0), "offsetLeft"), top:image_list.getoffset(config.$gallery.get(0), "offsetTop")}
				config.$leftnavbutton.css({left:/* config.offsets.left+ */config.defaultbuttons.leftnav[1]+'px', top:/* config.offsets.top+ */config.defaultbuttons.leftnav[2]+'px'})
				config.$rightnavbutton.css({right:/* left:config.offsets.left+config.$gallery.get(0).offsetWidth+ */config.defaultbuttons.rightnav[1]+'px', top:/* config.offsets.top+ */config.defaultbuttons.rightnav[2]+'px'})
			})
		}

		this.statusreport(config.galleryid)
		config.oninit()
		config.onslideaction(this)
	},

	stepTo:function(galleryid, pindex){ /*User entered pindex starts at 1 for intuitiveness. Internally pindex still starts at 0 */
		var config=image_list.configholder[galleryid]
		if (typeof config=="undefined"){
			alert("There's an error with your set up of Carousel Viewer \""+galleryid+ "\"!")
			return
		}
		var pindex=Math.min(pindex-1, config.paneloffsets.length-1)
		var endpoint=config.paneloffsets[pindex]+(pindex==0? 0 : config.beltoffset)
		if (config.panelbehavior.wraparound==false && config.defaultbuttons.enable==true){ //if carousel viewer should stop at first or last panel (instead of wrap back or forth)
			this.fadebuttons(config, pindex)
		}
		config.$belt.animate({left: -endpoint+'px'}, config.panelbehavior.speed, function(){config.onslideaction(this)})
		config.currentpanel=pindex
		this.statusreport(galleryid)
	},

	stepBy:function(galleryid, steps){ //isauto if defined indicates stepBy() is being called automatically
		var config=image_list.configholder[galleryid]
		if (typeof config=="undefined"){
			alert("There's an error with your set up of Carousel Viewer \""+galleryid+ "\"!")
			return
		}
		//alert(config.currentpanel);
		var direction=(steps>0)? 'forward' : 'back' //If "steps" is negative, that means backwards
		var pindex=config.currentpanel+steps //index of panel to stop at
		if (config.panelbehavior.wraparound==false){ //if carousel viewer should stop at first or last panel (instead of wrap back or forth)
			pindex=(direction=="back" && pindex<=0)? 0 : (direction=="forward")? Math.min(pindex, config.lastvisiblepanel) : pindex
			if (config.defaultbuttons.enable==true){ //if default nav buttons are enabled, fade them in and out depending on if at start or end of carousel
				image_list.fadebuttons(config, pindex)
			}
		}
		else{ //else, for normal stepBy behavior
			if (pindex>config.lastvisiblepanel && direction=="forward"){
				//if destination pindex is greater than last visible panel, yet we're currently not at the end of the carousel yet
				pindex=(config.currentpanel<config.lastvisiblepanel)? config.lastvisiblepanel : 0
			}
			else if (pindex<0 && direction=="back"){
				//if destination pindex is less than 0, yet we're currently not at the beginning of the carousel yet
				pindex=(config.currentpanel>0)? 0 : config.lastvisiblepanel /*wrap around left*/
			}
		}
		var endpoint=config.paneloffsets[pindex]+(pindex==0? 0 : config.beltoffset) //left distance for Belt DIV to travel to
		if (pindex==0 && direction=='forward' || config.currentpanel==0 && direction=='back' && config.panelbehavior.wraparound==true){ //decide whether to apply "push pull" effect
			config.$belt.animate({left: -config.paneloffsets[config.currentpanel]-(direction=='forward'? 100 : -30)+'px'}, 'normal', function(){
				config.$belt.animate({left: -endpoint+'px'}, config.panelbehavior.speed, function(){config.onslideaction(this)})
			})
		}
		else
			config.$belt.animate({left: -endpoint+'px'}, config.panelbehavior.speed, function(){config.onslideaction(this)})
		config.currentpanel=pindex
		this.statusreport(galleryid)
	},

	statusreport:function(galleryid){
		var config=image_list.configholder[galleryid]
		var startpoint=config.currentpanel //index of first visible panel
		var visiblewidth=0
		for (var endpoint=startpoint; endpoint<config.paneloffsets.length; endpoint++){ //index (endpoint) of last visible panel
			visiblewidth+=config.panelwidths[endpoint]
			if (visiblewidth>config.gallerywidth){
				break
			}
		}
		startpoint+=1 //format startpoint for user friendiness
		endpoint=(endpoint+1==startpoint)? startpoint : endpoint //If only one image visible on the screen and partially hidden, set endpoint to startpoint
		var valuearray=[startpoint, endpoint, config.panelwidths.length]
		for (var i=0; i<config.statusvars.length; i++){
			window[config.statusvars[i]]=valuearray[i] //Define variable (with user specified name) and set to one of the status values
			config.$statusobjs[i].text(valuearray[i]+" ") //Populate element on page with ID="user specified name" with one of the status values
		}
	},

	setup:function(config){
		//Disable Step Gallery scrollbars ASAP dynamically (enabled for sake of users with JS disabled)
		document.write('<style type="text/css">\n#'+config.galleryid+'{overflow: hidden;}\n</style>')
		jQuery(document).ready(function($){
			config.$gallery=$('#'+config.galleryid)
			config.gallerywidth=config.$gallery.width()
			config.offsets={left:image_list.getoffset(config.$gallery.get(0), "offsetLeft"), top:image_list.getoffset(config.$gallery.get(0), "offsetTop")}
			config.$belt=config.$gallery.find('.'+config.beltclass) //Find Belt DIV that contains all the panels
			config.$panels=config.$gallery.find('.'+config.panelclass) //Find Panel DIVs that each contain a slide
			config.panelbehavior.wraparound=config.panelbehavior.wraparound //if auto step enabled, set "wraparound" to true
			config.onpanelclick=(typeof config.onpanelclick=="undefined")? function(target){} : config.onpanelclick //attach custom "onpanelclick" event handler
			config.onslideaction=(typeof config.onslide=="undefined")? function(){} : function(beltobj){$(beltobj).stop(); config.onslide()} //attach custom "onslide" event handler
			config.oninit=(typeof config.oninit=="undefined")? function(){} : config.oninit //attach custom "oninit" event handler
			config.beltoffset=image_list.getCSSValue(config.$belt.css('marginLeft')) //Find length of Belt DIV's left margin
			config.statusvars=config.statusvars || []  //get variable names that will hold "start", "end", and "total" slides info
			config.$statusobjs=[$('#'+config.statusvars[0]), $('#'+config.statusvars[1]), $('#'+config.statusvars[2])]
			config.currentpanel=0
			image_list.configholder[config.galleryid]=config //store config parameter as a variable
			image_list.alignpanels(config) //align panels and initialize gallery
		}) //end document.ready
		jQuery(window).on('unload', function(){ //clean up
			jQuery.each(config, function(ai, oi){
				oi=null
			})
			config=null
		})
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////

function plog(msg, module){
	//if(console != undefined) console.log((module == undefined ? '' : module+' - ')+msg);
	return;
}

function checkPromo(id, clear_code){
	$('#res'+id).show();

	var formData = formToObj(document.forms["checkout-form"]);
	formData['mode'] = 'apply-promo';
	formData['fid'] = id;
	if(typeof clear_code != 'undefined'){
		formData['clear_code'] = 1;
		formData['code'] = 1;
	}else{
		formData['code'] = $('[name=fld'+id+']').val().toUpperCase();
	}
	delete formData['fld'+id];

	//_uPostForm('', {type: 'POST', url: location.href, data:{'mode': 'apply-promo', 'code': $('[name=fld'+id+']').val(), 'fid': id, 'ssid':$('input[name=ssid]').val()}});
	_uPostForm('', {type:'POST', url:decodeURIComponent('/shop/checkout'), data:formData});
}

function verifyEmail(id){
	var email = $('[name=fld'+id+']').val();
	_uPostForm('', {type:'POST', url:'/shop/checkout', data: {'mode': 'verify_email', 't': 'verify', 'email': email, 'field': id, 'ssid':$('input[name=ssid]').val()}});
}

function checkVerifyEmail(id){
	var code = $('[name=fld'+id+'code]').val();
	_uPostForm('', {type:'POST', url:'/shop/checkout', data: {'mode': 'verify_email', 't': 'check', 'code': code, 'field': id, 'ssid':$('input[name=ssid]').val()}});
}

/*
* Вывод информационных сообщения пользователям.
* Данная функция принимает следующий набор параметров:
*  wnd_msgs - сообщение, которое будет выведено пользователю. Сообщение может содержать HTML-теги форматирования.
*  wnd_title - заголовок окна сообщения, отображающегося в шапке.
*  wnd_type - тип сообщения. Может быть: «error» - ошибка, «warning» - предупреждение, «info» - информационное сообщение. Если тип не указан или указан тип, отличный от перечисленных, то считается, что сообщение общее, а не какого-то типа.
*  wnd_w - ширина окна.
*  wnd_h - высота окна.
*  wnd_opt - дополнительные параметры окна сообщения. Полный список параметров аналогичен списку параметров, принимаемых _uWnd() (http://helper.ucoz.ru/publ/coding/ujs/2-1-0-4).
*  wnd_name - уникальное имя окна. Нигде не отображается. Используется для дальнейшей работы с информационным окном с помощью функций _uWnd.
* */
function shop_alert(wnd_msgs, wnd_title, wnd_type, wnd_w, wnd_h, wnd_opt, wnd_name){
	var wnd_content = '';

	if(wnd_type == 'error'){
		wnd_content += '<div id="shop_wnd_error"></div><div id="shop_wnd_text">';
	}else{
		if(wnd_type == 'warning'){
			wnd_content += '<div id="shop_wnd_warning"></div><div id="shop_wnd_text">';
		}else{
			if(wnd_type == 'info'){
				wnd_content += '<div id="shop_wnd_info"></div><div id="shop_wnd_text">';
			}else{
				wnd_content += '<div>';
			}
		}
	}

	if(typeof wnd_name != 'string' || wnd_name == ''){
		wnd_name = 'shop_alert_window';
	}

	if(typeof wnd_msgs == 'string'){
		wnd_content += wnd_msgs;
	}else{
		if(typeof wnd_msgs == 'object'){
			wnd_content += '<ul>';
			for(msg in wnd_msgs) {
				wnd_content += '<li>'+wnd_msgs[msg]+'</li>';
			}
			wnd_content += '</ul>';
		}else{
			return;
		}
	}

	wnd_content += '</div>';

	wnd_opt = $.extend({
		align: 'left',			//выравнивание
		shadow: 1,				//тень
		header: 1,				//отображать ли шапку
		close: 1,				//отображать ли кнопку Close (закрыть).
		modal: 1,				//модальное окно
		popup: 1,				//закрывать ли окно при клике на пространстве вне окна.
		resize: 0,				//разрешить изменение размеров окна пользователем
		fixed: 0,				//разрешить изменение размеров окна пользователем
		closeonesc: 1,			//разрешить изменение размеров окна пользователем
		close: 1,
		icon: '',
		tm: 0,
		align: 'left'
	}, wnd_opt || {});

	var l = new _uWnd(
		wnd_name,
		wnd_title,
		wnd_w,
		wnd_h,
		wnd_opt,
		wnd_content
	);

	if (wnd_opt.tm > 0) {
		setTimeout("var w=_uWnd.all[" + l.idx + "];if(w)w.close();", wnd_opt.tm);
	}

	return l;
}

function formToObj(form) {
	var els = form ? form.elements : '', map = {}, el, i = 0;
	while (el = els[i++]){
		if (el.name != '' && !el.disabled){							// Элементы без имени и disabled не successful-controls
			switch (el.type.toLowerCase()) {
				case 'checkbox':
				case 'radio':										// Только выбранные (checked) checkbox'ы и
					if (el.checked) map[el.name] = el.value;		// radio-элементы считаются successful-controls
					break;
				case 'select-multiple':
					var opt = el.options, lst = [], j = 0, o;
					while (o = opt[j++])
						if (o.selected)								// Только выбранные (selected) опции (options)
							lst[lst.length] = o.value || o.text;	// считаются successful-controls
					if (lst.length)									// Добавляем масссив значений опции если он не пустой
						map[el.name] = lst;
					break;
				case 'select-one':									// select-one добавляем скаляром (не в масссив)
					if (!el.value) break;
				default:
					map[el.name] = el.value;
				case 'reset':										// reset не отправляется даже если имеет name
					break;
			}
		}
	}

	return map;
}

function priceFilter(f, v){
	if(_shopLockButtons()) return false;
	_shopFadeControl('goods_cont');
	_uPostForm('', {type:'POST', url:decodeURIComponent(document.location.href), data:{'mode':'filter', 'field':f, 'value':v}});
	return false;
}


/**
 * На странице списка заказов, после загрузки страницы,
 * если в ссылке есть параметр show_invoice=ХХХХ, открываем
 * попап с данными заказа.
 * Используется в виджете последних заказов в новой ПУ.
 */
$(document).ready(function() {
	if (location.pathname !== '/shop/invoices') {
		return;
	}

	var invoiceIdPair = location.search
		.substr(1)
		.split('&')
		.filter(function(pair) {
			return pair.indexOf('show_invoice=') === 0;
		})[0]
	;

	if (!invoiceIdPair) {
		return;
	}

	var invoiceId = invoiceIdPair.split('=')[1];

	if (!invoiceId) {
		return;
	}

	setTimeout(function() {
		window.invoiceShow(invoiceId);
	}, 100);
});
