## #!C:\laragon\bin\python\python-3.6.1\python.exe
from flask import (Flask, render_template, abort, jsonify, request,
                   redirect, url_for, logging, make_response)

# if app.debug is not True:
import logging
logging.basicConfig(handlers=[logging.FileHandler(filename="app.log", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    level=logging.INFO)

import re
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
#import orm

#debug/set_trace breakpoints
import pdb

app = Flask(__name__)
#app.config.from_pyfile(config_filename)

app.jinja_env.auto_reload = True
#TODO: Move to .env o.Ae.
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///ztf_alerts_manual.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
#TODO: Moce to module
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

db = SQLAlchemy(app)
class Ztf(db.Model):
    __tablename__ = 'indextable'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    candid = db.Column(db.Integer)
    objectId = db.Column(db.String)
    jd = db.Column(db.Float)
    filter = db.Column(db.Integer)
    ra = db.Column(db.Float)
    dec = db.Column(db.Float)
    magpsf = db.Column(db.Float)
    magap = db.Column(db.Float)

    # @property
    # def ra(self):
    #     ra = shape.to_shape(self.location).x
    #     if ra < 0:
    #         ra = ra + 360
    #     return ra
    # @property
    # def dec(self):
    #     return shape.to_shape(self.location).y

    def __str__(self):
        return self.objectId

class Features(db.Model):
    __tablename__ = 'featuretable'
    date = db.Column(db.Integer)
    candid = db.Column(db.Integer)
    objectId = db.Column(db.String, primary_key=True) #not an actual PK
    A_sf_g = db.Column(db.Float)
    gamma_sf_g = db.Column(db.Float)
    A_sf_r = db.Column(db.Float)
    gamma_sf_r = db.Column(db.Float)
    sigmaDRW_g = db.Column(db.Float)
    tauDRW_g = db.Column(db.Float)
    sigmaDRW_r = db.Column(db.Float)
    tauDRW_r = db.Column(db.Float)
    gr = db.Column(db.Float)
    ri = db.Column(db.Float)
    A_r = db.Column(db.Float)
    A_g = db.Column(db.Float)
    P = db.Column(db.Float)
    H1 = db.Column(db.Float)
    R21 = db.Column(db.Float)
    R31 = db.Column(db.Float)
    phi21 = db.Column(db.Float)
    phi31 = db.Column(db.Float)
    gamma1 = db.Column(db.Float)
    gamma2 = db.Column(db.Float)
    K = db.Column(db.Float)
    Q31 = db.Column(db.Float)
    p10 = db.Column(db.Float)
    p90 = db.Column(db.Float)

class Classification(db.Model):
    __tablename__ = 'classificationtable'
    date = db.Column(db.Integer)
    candid = db.Column(db.Integer)
    objectId = db.Column(db.String, primary_key=True) #not an actual PK
    Simbad_name = db.Column(db.String)
    Simbad_objecttype = db.Column(db.String)
    PS1_RRL_P = db.Column(db.Float)
    PS1_RRL_helio_dist = db.Column(db.Float)
    AllWISE_name = db.Column(db.String)
    AllWISE_W1mag = db.Column(db.Float)
    AllWISE_W2mag = db.Column(db.Float)
    AllWISE_W3mag = db.Column(db.Float)
    AllWISE_W4mag = db.Column(db.Float)
    twoMASS_name = db.Column(db.String)
    twoMASS_angDist = db.Column(db.Float)
    twoMASS_Jmag = db.Column(db.Float)
    twoMASS_Hmag = db.Column(db.Float)
    twoMASS_Kmag = db.Column(db.Float)
    twoMASS_Qflg = db.Column(db.Float)
    twoMASS_Rflg = db.Column(db.Float)
    twoMASS_Aflg = db.Column(db.Float)
    ASASSN_name = db.Column(db.String)
    ASASSN_OtherNames = db.Column(db.String)
    ASASSN_amplitude = db.Column(db.Float)
    ASASSN_period = db.Column(db.Float)
    ASASSN_Type = db.Column(db.String)
    ASASSN_class_probability = db.Column(db.Float)
    ASASSN_Periodic = db.Column(db.Float)
    ASASSN_VClassified = db.Column(db.Float)
    NED_name = db.Column(db.String)
    NED_ra = db.Column(db.Float)
    NED_de = db.Column(db.Float) #TODO: Should be NED_dec instead
    NED_Type = db.Column(db.String)
    NED_separation_arcmin = db.Column(db.Float)
    NED_associated = db.Column(db.Float)
    VSX_OID = db.Column(db.String)
    VSX_Name = db.Column(db.String)
    VSX_V = db.Column(db.Integer)
    VSX_Type = db.Column(db.String)


#v0: Access SQLite directly
#from yourapplication.model import db
#db.init_app(app)
#from db_access import db
#import db_access
#v1: Access SQLite via SQLAlchemy -> flask-sqlalchemy

#Jinja Filter
@app.template_filter('astro_filter')
def astro_filter(num):
    if (num == 1):
        return "g"
    elif (num == 2):
        return "r"
    elif (num == 3):
        return "i"

@app.route('/', methods=['GET', 'POST'])
def start():
    #app.logger.info('Info')
    #app.logger.warning('Warn')
    #logging.error('Exception occurred', exc_info=True) #or: logging.exception()
    logging.info('Request with request_args:' + json.dumps(request.args))
    #pdb.set_trace()
    page = request.args.get('page', 1, type=int)

    data = []
    filter_warning_message = ''
    if request.method == 'GET':
        query = db.session.query(Ztf)
        # Return alerts with a brightness greater than the given value. Ex: ?magpsf=17,18 (range:17-18)
        
        if request.args.get('date'):
            date_input = extract_numbers(request.args.get('date'))
            if date_input != None:
                query = extract_float_filter(date_input, Ztf.date, query)
            else:
                filter_warning_message += 'Date filter cannot be applied - Enter a valid 8-digit integer date of the form yyyymmdd, e.g. "20201207", or range, e.g., "20201207 20201209". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('candid'):
            candid_input = extract_numbers(request.args.get('candid'))
            if candid_input != None:
                query = query.filter(Ztf.candid == int(request.args.get('candid')))
            else:
                 filter_warning_message += 'Candid filter cannot be applied - Enter a valid integer, e.g. "1436374650315010006". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('objectId'):
            query = query.filter(Ztf.objectId == request.args.get('objectId'))

        if request.args.get('jd'):
            jd_input = extract_numbers(request.args.get('jd'))
            if jd_input != None:
                query = extract_float_filter(jd_input, Ztf.jd, query)
            else:
                filter_warning_message += 'Jd filter cannot be applied - Enter a valid number, e.g., "2459190.8746528", or range, e.g., "2459190.84 2459190.86". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('filter'):
            query = query.filter(Ztf.filter == int(request.args.get('filter'))) # 1:g, 2:r, 3:i

        if request.args.get('ra'):
            ra_input = extract_numbers(request.args.get('ra'))
            if ra_input != None:
                query = extract_float_filter(ra_input, Ztf.ra, query)
            else:
                filter_warning_message += 'Ra filter cannot be applied - Enter a valid number, e.g., "118.61421", or range, e.g., "80 90". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('dec'):
            dec_input = extract_numbers(request.args.get('dec'))
            if dec_input != None:
                query = extract_float_filter(dec_input, Ztf.dec, query)
            else:
                filter_warning_message += 'Dec filter cannot be applied - Enter a valid number, e.g., "-20.02131", or range, e.g., "18.8 19.4". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('magpsf'):
            magpsf_input = extract_numbers(request.args.get('magpsf'))
            if magpsf_input != None:
                query = extract_float_filter(magpsf_input, Ztf.magpsf, query)
            else:
                filter_warning_message += 'Magpsf filter cannot be applied - Enter a valid number, e.g., "18.84", or range, e.g., "18.8 19.4". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('magap'):
            magap_input = extract_numbers(request.args.get('magap'))
            if magap_input != None:
                query = extract_float_filter(magap_input, Ztf.magap, query)
            else:
                filter_warning_message += 'Magap filter cannot be applied - Enter a valid number, e.g., "19.49", or range, e.g., "18.8 19.4". You can filter the columns by entering values and then click the "Filter" button.'

        #Sort order by date
        if request.args.get('sort__date'):
            sort__date_order = request.args.get('sort__date')
            if sort__date_order == 'desc':
                query = query.order_by(Ztf.date.desc())
            if sort__date_order == 'asc':
                query = query.order_by(Ztf.date.asc())

        #Sort order by candid
        if request.args.get('sort__candid'):
            sort__candid_order = request.args.get('sort__candid')
            if sort__candid_order == 'desc':
                query = query.order_by(Ztf.candid.desc())
            if sort__candid_order == 'asc':
                query = query.order_by(Ztf.candid.asc())
        
        #Sort order by objectId
        if request.args.get('sort__objectId'):
            sort__objectId_order = request.args.get('sort__objectId')
            if sort__objectId_order == 'desc':
                query = query.order_by(Ztf.objectId.desc())
            if sort__objectId_order == 'asc':
                query = query.order_by(Ztf.objectId.asc())

        #Sort order by jd
        if request.args.get('sort__jd'):
            sort__jd_order = request.args.get('sort__jd')
            if sort__jd_order == 'desc':
                query = query.order_by(Ztf.jd.desc())
            if sort__jd_order == 'asc':
                query = query.order_by(Ztf.jd.asc())

        #Sort order by ra
        if request.args.get('sort__ra'):
            sort__ra_order = request.args.get('sort__ra')
            if sort__ra_order == 'desc':
                query = query.order_by(Ztf.ra.desc())
            if sort__ra_order == 'asc':
                query = query.order_by(Ztf.ra.asc())

        #Sort order by dec
        if request.args.get('sort__dec'):
            sort__dec_order = request.args.get('sort__dec')
            if sort__dec_order == 'desc':
                query = query.order_by(Ztf.dec.desc())
            if sort__dec_order == 'asc':
                query = query.order_by(Ztf.dec.asc())

        #Sort order by magpsf
        if request.args.get('sort__magpsf'):
            sort__magpsf_order = request.args.get('sort__magpsf')
            if sort__magpsf_order == 'desc':
                query = query.order_by(Ztf.magpsf.desc())
            if sort__magpsf_order == 'asc':
                query = query.order_by(Ztf.magpsf.asc())

        #Sort order by magap
        if request.args.get('sort__magap'):
            sort__magap_order = request.args.get('sort__magap')
            if sort__magap_order == 'desc':
                query = query.order_by(Ztf.magap.desc())
            if sort__magap_order == 'asc':
                query = query.order_by(Ztf.magap.asc())



        #latest = db.session.query(Ztf).order_by(Ztf.jd.desc()).first() # ? to show latest update date
        paginator = query.paginate(page, 100, True)
        #pdb.set_trace()
        # response = {
        #     'has_next': paginator.has_next,
        #     'has_prev': paginator.has_prev,
        #     'results': Alert.serialize_list(paginator.items)
        # }
        #pdb.set_trace()

    return render_template(
        "main.html",
        total_queries=paginator.total,
        table=paginator.items,
        page=paginator.page,
        has_next=paginator.has_next,
        last_page=paginator.pages,
        query_string=re.sub('&page=\\d+', '', request.query_string.decode('ascii')), # ? b'' binary string
        filter_warning = filter_warning_message
    )

import pandas as pd
from pathlib import Path

@app.route('/generate_lightcurve', methods=['GET'])
def generate_lightcurve():
    objectId = request.args.get('objectId')
    print('objectId: ', objectId)
    #generate lightcurve, store it on the server
    my_file = Path('static/_ZTF_lightcurves_concat/'+objectId+'.csv')
    lc_plot_uri = '/static/img/_ZTF_lc_plots/'+objectId+'.png' #expected result path
    if my_file.is_file():
        df = pd.read_csv(my_file)
        foldername = Path("static/img/_ZTF_lc_plots")
        
        dflc = generate_dcmag_lightcurve(df)
        lc_plot_uri = plot_lightcurve(dflc, foldername, objectId)
    else:
        lc_plot_uri = '/static/img/_ZTF_lc_plots/missing_file.png' #missing CSV #TODO: This shoud work now as handled in JS CsvExists(), TEST!
    #print('/static/img/_ZTF_lc_plots/'+objectId+'.png')
    print(lc_plot_uri)
    response = make_response(lc_plot_uri, 200)
    response.mimetype = "text/plain"
    return response



#NOTE: Features are filter by objectId & candid
@app.route('/query_features', methods=['GET'])
def query_features():
    objectId = request.args.get('objectId')
    candid = request.args.get('candid')
    print('objectId: %s; candid: %s' % (objectId, candid))

    feature_query = db.session.query(Features)
    feature_query = feature_query.filter(Features.objectId == objectId)
    feature_query = feature_query.filter(Features.candid == candid)

    data = object_as_dict(feature_query.first())
    print(data)
    
    response = app.response_class(
        response=json.dumps(data), #TODO? array[] with single row when using BootstrapTable?
        status=200,
        mimetype='application/json'
    )
    return response

#NOTE: #classification filter by objectId
@app.route('/query_classification', methods=['GET'])
def query_classification():
    objectId = request.args.get('objectId')
    print('objectId: ', objectId)

    feature_query = db.session.query(Classification)
    feature_query = feature_query.filter(Classification.objectId == objectId)
    data = object_as_dict(feature_query.first())
    
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(debug=True)

# Helper

def extract_numbers(text):
    #number with optional deciaml point
    regex = r"[<>]?[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))"
    matches = re.findall(regex, text)
    if len(matches) < 1:
        return None
    elif len(matches) == 1:
        return [matches[0]]
    else:
        return list(map(lambda m: m.replace('>', '').replace('<', ''), matches[0:2]))
         #TODO: we either want to remove </> or add them if missing to be consistent (TBD)

def extract_float_filter(input_field, db_field, query):
    float_func = lambda x: float(x)
    return extract_filter(input_field, db_field, query, float_func)

def extract_int_filter(input_field, db_field, query):
    int_func = lambda x: int(x)
    return extract_filter(input_field, db_field, query, int_func)

def extract_filter(input_field, db_field, query, convert_callback):
    #pdb.set_trace()
    if len(input_field) == 1:
        if '>' in input_field[0]:
            query = query.filter(db_field >= convert_callback(input_field[0].replace('>', '')))
        elif '<' in input_field[0]:
            query = query.filter(db_field <= convert_callback(input_field[0].replace('<', '')))
        else:
            query = query.filter(db_field == convert_callback(input_field[0]))
    else: #2 inputs
        input_field.sort()  #REM: Ensure >min <max order
        query = query.filter(db_field >= convert_callback(input_field[0]))
        query = query.filter(db_field <= convert_callback(input_field[1]))
    return query


import numpy as np
import matplotlib.pyplot as plt

def generate_dcmag_lightcurve(dflc):

	len_good = ( len(  dflc[dflc.isdiffpos.notnull() & (dflc.magnr>0) & (dflc.magpsf>0)] ) )
	print('len_good: ',  len_good)
	#len_good = ( len(  dflc[dflc.isdiffpos.notnull()] ) )
	#print ('isdiffpos not null:', len_good)
	#print( dflc[dflc.isdiffpos.notnull()])
	
	if(len_good>1):
		
		#print(dflc['distnr'])
		#print('generate_dcmag_lightcurve')
		#print(np.max(dflc['distnr']))
		# confirm that the nearest reference source from ZTF is  coincident
		if (np.max(dflc['distnr']<1.5)):
			
				
			grp = dflc.groupby(['fid','field','rcid'])
			#print('grp[magnr]')
			#print(grp['magnr'])
			
			
			#impute only possible if at min 2 for each fid,field
			
			#impute_magnr = grp['magnr'].agg(lambda x: np.median(x[np.isfinite(x)]))
			try:
				impute_magnr = grp['magnr'].agg(lambda x: np.median(x[pd.notnull(x)]))
			
			
				#print('impute_magnr: ', impute_magnr)
			#impute_sigmagnr = grp['sigmagnr'].agg(lambda x: np.median(x[np.isfinite(x)]))
			
				impute_sigmagnr = grp['sigmagnr'].agg(lambda x: np.median(x[pd.notnull(x)]))
				
				for idx, grpi in grp:
					#w = np.isnan(grpi['magnr'])
					
					w = pd.isnull(grpi['magnr'])
					
					w2 = grpi[w].index
					dflc.loc[w2,'magnr'] = impute_magnr[idx]
					dflc.loc[w2,'sigmagnr'] = impute_sigmagnr[idx]
					
			except:
				pass
			
			#print(impute_sigmagnr)

			
			dflc['sign'] = 2* (dflc['isdiffpos'] == 't') - 1

			u = (10**(-0.4*dflc['magnr']) + dflc['sign'] * 10**(-0.4*dflc['magpsf'])).astype(np.float64)
			
			
			dflc['dc_mag'] = -2.5 * np.log10(u)
			dflc['dc_sigmag'] = np.sqrt(
			(10**(-0.4*dflc['magnr'].astype(np.float64))* dflc['sigmagnr'].astype(np.float64)) **2. + 
			(10**(-0.4*dflc['magpsf'].astype(np.float64)) * dflc['sigmapsf'].astype(np.float64))**2.) / u
			dflc['dc_mag_ulim'] = -2.5 * np.log10(10**(-0.4*dflc['magnr'].astype(np.float64)) + 10**(-0.4*dflc['diffmaglim'].astype(np.float64)))
			dflc['dc_mag_llim'] = -2.5 * np.log10(10**(-0.4*dflc['magnr'].astype(np.float64)) - 10**(-0.4*dflc['diffmaglim'].astype(np.float64)))
			
	return dflc	


def plot_lightcurve(dflc, lc_plot_folder, objectId):
	len_good = ( len(  dflc[dflc.isdiffpos.notnull() & (dflc.magnr>0) & (dflc.magpsf>0)] ) )
	#len_good = ( len(  dflc[dflc.isdiffpos.notnull()] ) )
	##print ('isdiffpos not null:', len_good)
	#print( dflc[dflc.isdiffpos.notnull()])
	
	if(len_good>1):
		##print(dflc['distnr'])			
		filter_color = {1:'green', 2:'red', 3:'gold'}
		#if days_ago:
			#now = Time.now().jd
			#t = dflc.jd - now
			#xlabel = 'Days Ago'
		#else:
			#t = dflc.jd
			#xlabel = 'Time (JD)'
		
		t = dflc.jd - 2400000.5
		

		fig = plt.figure(figsize=(5.5,3))
		
		fig.subplots_adjust(left=0.13, right=0.95, top=0.92, bottom=0.17, hspace = 0.4)

		#for fid, color in filter_color.items():
			## plot detections in this filter:
			#w = (dflc.fid == fid) & ~dflc.magpsf.isnull()
			#if np.sum(w):
				#plt.errorbar(t[w],dflc.loc[w,'dc_mag'], dflc.loc[w,'dc_sigmag'],fmt='.',color=color)
			#wnodet = (dflc.fid == fid) & dflc.magpsf.isnull()
			#if np.sum(wnodet):
				#plt.scatter(t[wnodet],dflc.loc[wnodet,'dc_mag_ulim'], marker='v',color=color,alpha=0.25)
				#plt.scatter(t[wnodet],dflc.loc[wnodet,'dc_mag_llim'], marker='^',color=color,alpha=0.25)
		
		
		#print('plot_lightcurve')
		#print(np.max(dflc['distnr']))
		
		
		if (np.max(dflc['distnr']<1.5)):
					
						
			for fid, color in filter_color.items():
				# plot detections in this filter:
				w = (dflc.fid == fid) & ~dflc.magpsf.isnull()
				#print(color)
				#print(w)
				#print(np.sum(w))
				if np.sum(w):
				#	print('plot')
					plt.errorbar(t[w],dflc.loc[w,'dc_mag'], dflc.loc[w,'dc_sigmag'],fmt='.',color=color)
				wnodet = (dflc.fid == fid) & dflc.magpsf.isnull()
				
				#print(wnodet)
				#print(np.sum(wnodet))
				if np.sum(wnodet):
				#	print('plot')
					plt.scatter(t[wnodet],dflc.loc[wnodet,'dc_mag_ulim'], marker='v',color=color,alpha=0.25)
					plt.scatter(t[wnodet],dflc.loc[wnodet,'dc_mag_llim'], marker='^',color=color,alpha=0.25)
					
					plt.ylabel('dc mag')		

		else:
			
			for fid, color in filter_color.items():
				# plot detections in this filter:
				w = (dflc.fid == fid) & ~dflc.magpsf.isnull()
				if np.sum(w):
					plt.errorbar(t[w],dflc.loc[w,'magpsf'], dflc.loc[w,'sigmapsf'],fmt='.',color=color)
				wnodet = (dflc.fid == fid) & dflc.magpsf.isnull()
				if np.sum(wnodet):
					plt.scatter(t[wnodet],dflc.loc[wnodet,'diffmaglim'], marker='v',color=color,alpha=0.25)
				plt.ylabel('psf mag')		
					
		
		plt.gca().invert_yaxis()

		plt.xlabel('time (MJD)')
		plt.ylabel('dc Magnitude')		
		#pdb.set_trace()
		lc_plot_fullpath = str(lc_plot_folder) + '/%s.png' %(objectId)
		fig.savefig(lc_plot_fullpath,dpi = 100)
		plt.close('all')
		return lc_plot_fullpath
	else:
		return '/' + str(lc_plot_folder).replace('\\', '/') + '/not_enough_data_for_analysis.png'