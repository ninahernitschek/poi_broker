## #!C:\laragon\bin\python\python-3.6.1\python.exe
import random
from flask import (Flask, render_template, abort, jsonify, request, Response,
                   redirect, url_for, logging, make_response)

# if app.debug is not True:
import logging
logging.basicConfig(handlers=[logging.FileHandler(filename="app.log", 
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    level=logging.INFO)
from astropy.time import Time
import re
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
#import orm

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import Legend

#debug/set_trace breakpoints
import pdb

from pprint import pprint

import os

app = Flask(__name__)
#app.config.from_pyfile(config_filename)

app.jinja_env.auto_reload = True



current_dirs_parent = os.path.dirname(os.getcwd())
print(current_dirs_parent)

db_path = current_dirs_parent + '/_broker_db/ztf_alerts_stream.db'
db_uri = 'sqlite:///{}'.format(db_path)


#TODO: Move to .env o.Ae.
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    SQLALCHEMY_DATABASE_URI=db_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
#SQLALCHEMY_DATABASE_URI='sqlite:///ztf_alerts_stream.db',

#TODO: Move to module
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

db = SQLAlchemy(app)
class Ztf(db.Model):
    
    #OLD:
    #__tablename__ = 'indextable'
    #id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.Integer)
    #candid = db.Column(db.Integer)
    #objectId = db.Column(db.String)
    #jd = db.Column(db.Float)
    #filter = db.Column(db.Integer)
    #ra = db.Column(db.Float)
    #dec = db.Column(db.Float)
    #magpsf = db.Column(db.Float)
    #magap = db.Column(db.Float)
    
    __tablename__ = 'featuretable'
    #id = db.Column(db.Integer, primary_key=True)
    date_alert_mjd = db.Column(db.Float, primary_key=True)
    alert_id = db.Column(db.String, primary_key=True)
    ztf_object_id = db.Column(db.String)
    locus_id = db.Column(db.String, primary_key=True)
    locus_ra = db.Column(db.Float)
    locus_dec = db.Column(db.Float)
    ant_mag_corrected = db.Column(db.Float)
    ant_passband = db.Column(db.String)
    feature_amplitude_magn_r = db.Column(db.Float)
    feature_anderson_darling_normal_magn_r = db.Column(db.Float)
    feature_beyond_1_std_magn_r = db.Column(db.Float)
    feature_beyond_2_std_magn_r = db.Column(db.Float)
    feature_cusum_magn_r = db.Column(db.Float)
    feature_eta_e_magn_r = db.Column(db.Float)
    feature_inter_percentile_range_2_magn_r = db.Column(db.Float)
    feature_inter_percentile_range_10_magn_r = db.Column(db.Float)
    feature_inter_percentile_range_25_magn_r = db.Column(db.Float)
    feature_kurtosis_magn_r = db.Column(db.Float)
    feature_linear_fit_slope_magn_r = db.Column(db.Float)
    feature_linear_fit_slope_sigma_magn_r = db.Column(db.Float)
    feature_linear_fit_reduced_chi2_magn_r = db.Column(db.Float)
    feature_linear_trend_magn_r = db.Column(db.Float)
    feature_linear_trend_sigma_magn_r = db.Column(db.Float)
    feature_magnitude_percentage_ratio_40_5_magn_r = db.Column(db.Float)
    feature_magnitude_percentage_ratio_20_5_magn_r = db.Column(db.Float)
    feature_maximum_slope_magn_r = db.Column(db.Float)
    feature_mean_magn_r = db.Column(db.Float)
    feature_median_absolute_deviation_magn_r = db.Column(db.Float)
    feature_percent_amplitude_magn_r = db.Column(db.Float)
    feature_percent_difference_magnitude_percentile_5_magn_r = db.Column(db.Float)
    feature_percent_difference_magnitude_percentile_10_magn_r = db.Column(db.Float)
    feature_median_buffer_range_percentage_10_magn_r = db.Column(db.Float)
    feature_median_buffer_range_percentage_20_magn_r = db.Column(db.Float)
    feature_period_0_magn_r = db.Column(db.Float)
    feature_period_s_to_n_0_magn_r = db.Column(db.Float)
    feature_period_1_magn_r = db.Column(db.Float)
    feature_period_s_to_n_1_magn_r = db.Column(db.Float)
    feature_period_2_magn_r = db.Column(db.Float)
    feature_period_s_to_n_2_magn_r = db.Column(db.Float)
    feature_period_3_magn_r = db.Column(db.Float)
    feature_period_s_to_n_3_magn_r = db.Column(db.Float)
    feature_period_4_magn_r = db.Column(db.Float)
    feature_period_s_to_n_4_magn_r = db.Column(db.Float)
    feature_periodogram_amplitude_magn_r = db.Column(db.Float)
    feature_periodogram_beyond_2_std_magn_r = db.Column(db.Float)
    feature_periodogram_beyond_3_std_magn_r = db.Column(db.Float)
    feature_periodogram_standard_deviation_magn_r = db.Column(db.Float)
    feature_chi2_magn_r = db.Column(db.Float)
    feature_skew_magn_r = db.Column(db.Float)
    feature_standard_deviation_magn_r = db.Column(db.Float)
    feature_stetson_k_magn_r = db.Column(db.Float)
    feature_weighted_mean_magn_r = db.Column(db.Float)
    feature_anderson_darling_normal_flux_r = db.Column(db.Float)
    feature_cusum_flux_r = db.Column(db.Float)
    feature_eta_e_flux_r = db.Column(db.Float)
    feature_excess_variance_flux_r = db.Column(db.Float)
    feature_kurtosis_flux_r = db.Column(db.Float)
    feature_mean_variance_flux_r = db.Column(db.Float)
    feature_chi2_flux_r = db.Column(db.Float)
    feature_skew_flux_r = db.Column(db.Float)
    feature_stetson_k_flux_r = db.Column(db.Float)
    feature_amplitude_magn_g = db.Column(db.Float)
    feature_anderson_darling_normal_magn_g = db.Column(db.Float)
    feature_beyond_1_std_magn_g = db.Column(db.Float)
    feature_beyond_2_std_magn_g = db.Column(db.Float)
    feature_cusum_magn_g = db.Column(db.Float)
    feature_eta_e_magn_g = db.Column(db.Float)
    feature_inter_percentile_range_2_magn_g = db.Column(db.Float)
    feature_inter_percentile_range_10_magn_g = db.Column(db.Float)
    feature_inter_percentile_range_25_magn_g = db.Column(db.Float)
    feature_kurtosis_magn_g = db.Column(db.Float)
    feature_linear_fit_slope_magn_g = db.Column(db.Float)
    feature_linear_fit_slope_sigma_magn_g = db.Column(db.Float)
    feature_linear_fit_reduced_chi2_magn_g = db.Column(db.Float)
    feature_linear_trend_magn_g = db.Column(db.Float)
    feature_linear_trend_sigma_magn_g = db.Column(db.Float)
    feature_magnitude_percentage_ratio_40_5_magn_g = db.Column(db.Float)
    feature_magnitude_percentage_ratio_20_5_magn_g = db.Column(db.Float)
    feature_maximum_slope_magn_g = db.Column(db.Float)
    feature_mean_magn_g = db.Column(db.Float)
    feature_median_absolute_deviation_magn_g = db.Column(db.Float)
    feature_percent_amplitude_magn_g = db.Column(db.Float)
    feature_percent_difference_magnitude_percentile_5_magn_g = db.Column(db.Float)
    feature_percent_difference_magnitude_percentile_10_magn_g = db.Column(db.Float)
    feature_median_buffer_range_percentage_10_magn_g = db.Column(db.Float)
    feature_median_buffer_range_percentage_20_magn_g = db.Column(db.Float)
    feature_period_0_magn_g = db.Column(db.Float)
    feature_period_s_to_n_0_magn_g = db.Column(db.Float)
    feature_period_1_magn_g = db.Column(db.Float)
    feature_period_s_to_n_1_magn_g = db.Column(db.Float)
    feature_period_2_magn_g = db.Column(db.Float)
    feature_period_s_to_n_2_magn_g = db.Column(db.Float)
    feature_period_3_magn_g = db.Column(db.Float)
    feature_period_s_to_n_3_magn_g = db.Column(db.Float)
    feature_period_4_magn_g = db.Column(db.Float)
    feature_period_s_to_n_4_magn_g = db.Column(db.Float)
    feature_periodogram_amplitude_magn_g = db.Column(db.Float)
    feature_periodogram_beyond_2_std_magn_g = db.Column(db.Float)
    feature_periodogram_beyond_3_std_magn_g = db.Column(db.Float)
    feature_periodogram_standard_deviation_magn_g = db.Column(db.Float)
    feature_chi2_magn_g = db.Column(db.Float)
    feature_skew_magn_g = db.Column(db.Float)
    feature_standard_deviation_magn_g = db.Column(db.Float)
    feature_stetson_k_magn_g = db.Column(db.Float)
    feature_weighted_mean_magn_g = db.Column(db.Float)
    feature_anderson_darling_normal_flux_g = db.Column(db.Float)
    feature_cusum_flux_g = db.Column(db.Float)
    feature_eta_e_flux_g = db.Column(db.Float)
    feature_excess_variance_flux_g = db.Column(db.Float)
    feature_kurtosis_flux_g = db.Column(db.Float)
    feature_mean_variance_flux_g = db.Column(db.Float)
    feature_chi2_flux_g = db.Column(db.Float)
    feature_skew_flux_g = db.Column(db.Float)
    feature_stetson_k_flux_g = db.Column(db.Float)
		

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
        return self.ztf_object_id

#OLD:
#class Features(db.Model):
    #__tablename__ = 'featuretable'
    #date = db.Column(db.Integer)
    #candid = db.Column(db.Integer)
    #objectId = db.Column(db.String, primary_key=True) #not an actual PK
    #A_sf_g = db.Column(db.Float)
    #gamma_sf_g = db.Column(db.Float)
    #A_sf_r = db.Column(db.Float)
    #gamma_sf_r = db.Column(db.Float)
    #sigmaDRW_g = db.Column(db.Float)
    #tauDRW_g = db.Column(db.Float)
    #sigmaDRW_r = db.Column(db.Float)
    #tauDRW_r = db.Column(db.Float)
    #gr = db.Column(db.Float)
    #ri = db.Column(db.Float)
    #A_r = db.Column(db.Float)
    #A_g = db.Column(db.Float)
    #P = db.Column(db.Float)
    #H1 = db.Column(db.Float)
    #R21 = db.Column(db.Float)
    #R31 = db.Column(db.Float)
    #phi21 = db.Column(db.Float)
    #phi31 = db.Column(db.Float)
    #gamma1 = db.Column(db.Float)
    #gamma2 = db.Column(db.Float)
    #K = db.Column(db.Float)
    #Q31 = db.Column(db.Float)
    #p10 = db.Column(db.Float)
    #p90 = db.Column(db.Float)

#OLD:
#class Classification(db.Model):
    #__tablename__ = 'classificationtable'
    #date = db.Column(db.Integer)
    #candid = db.Column(db.Integer)
    #objectId = db.Column(db.String, primary_key=True) #not an actual PK
    #Simbad_name = db.Column(db.String)
    #Simbad_objecttype = db.Column(db.String)
    #PS1_RRL_P = db.Column(db.Float)
    #PS1_RRL_helio_dist = db.Column(db.Float)
    #AllWISE_name = db.Column(db.String)
    #AllWISE_W1mag = db.Column(db.Float)
    #AllWISE_W2mag = db.Column(db.Float)
    #AllWISE_W3mag = db.Column(db.Float)
    #AllWISE_W4mag = db.Column(db.Float)
    #twoMASS_name = db.Column(db.String)
    #twoMASS_angDist = db.Column(db.Float)
    #twoMASS_Jmag = db.Column(db.Float)
    #twoMASS_Hmag = db.Column(db.Float)
    #twoMASS_Kmag = db.Column(db.Float)
    #twoMASS_Qflg = db.Column(db.Float)
    #twoMASS_Rflg = db.Column(db.Float)
    #twoMASS_Aflg = db.Column(db.Float)
    #ASASSN_name = db.Column(db.String)
    #ASASSN_OtherNames = db.Column(db.String)
    #ASASSN_amplitude = db.Column(db.Float)
    #ASASSN_period = db.Column(db.Float)
    #ASASSN_Type = db.Column(db.String)
    #ASASSN_class_probability = db.Column(db.Float)
    #ASASSN_Periodic = db.Column(db.Float)
    #ASASSN_VClassified = db.Column(db.Float)
    #NED_name = db.Column(db.String)
    #NED_ra = db.Column(db.Float)
    #NED_de = db.Column(db.Float) #TODO: Should be NED_dec instead
    #NED_Type = db.Column(db.String)
    #NED_separation_arcmin = db.Column(db.Float)
    #NED_associated = db.Column(db.Float)
    #VSX_OID = db.Column(db.String)
    #VSX_Name = db.Column(db.String)
    #VSX_V = db.Column(db.Integer)
    #VSX_Type = db.Column(db.String)


#v0: Access SQLite directly
#from yourapplication.model import db
#db.init_app(app)
#from db_access import db
#import db_access
#v1: Access SQLite via SQLAlchemy -> flask-sqlalchemy

#Jinja Filter
# @app.template_filter('astro_filter')
# def astro_filter(num):
#     if (num == 1):
#         return "g"
#     elif (num == 2):
#         return "r"
#     elif (num == 3):
#         return "i"

@app.template_filter('astro_filter')
def astro_filter(num):
    return 'tbd'

@app.template_filter('mag_filter')
def mag_filter(num):
    if num: 
        return round(num,3)
    # else:
    #     return ''

@app.template_filter('format_mjd_readable')
def format_mjd_readable(value):
    #return (value / 86400000) + 40587
    jdate = value+2400000.5
    t = Time(jdate, format='jd')
    return t.isot #in UTC

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
        
        if request.args.get('date_alert_mjd'):
            date_input = extract_numbers(request.args.get('date_alert_mjd'))
            if date_input != None:
                query = extract_float_filter(date_input, Ztf.date_alert_mjd, query)
            else:
                filter_warning_message += 'Date filter cannot be applied - Enter a valid 8-digit integer date of the form yyyymmdd, e.g. "20201207", or range, e.g., "20201207 20201209". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('alert_id'):
            candid_input = extract_numbers(request.args.get('alert_id'))
            if candid_input != None:
                query = query.filter(Ztf.alert_id == int(request.args.get('alert_id')))
            else:
                 filter_warning_message += 'Candid filter cannot be applied - Enter a valid integer, e.g. "1436374650315010006". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('ztf_object_id'):
            query = query.filter(Ztf.ztf_object_id == request.args.get('ztf_object_id'))

        #if request.args.get('jd'):
            #jd_input = extract_numbers(request.args.get('jd'))
            #if jd_input != None:
                #query = extract_float_filter(jd_input, Ztf.jd, query)
            #else:
                #filter_warning_message += 'Jd filter cannot be applied - Enter a valid number, e.g., "2459190.8746528", or range, e.g., "2459190.84 2459190.86". You can filter the columns by entering values and then click the "Filter" button.'

        #if request.args.get('filter'):
            #query = query.filter(Ztf.filter == int(request.args.get('filter'))) # 1:g, 2:r, 3:i

        if request.args.get('locus_id'):
            query = query.filter(Ztf.locus_id == request.args.get('locus_id'))

        if request.args.get('locus_ra'):
            ra_input = extract_numbers(request.args.get('locus_ra'))
            if ra_input != None:
                query = extract_float_filter(ra_input, Ztf.locus_ra, query)
            else:
                filter_warning_message += 'Ra filter cannot be applied - Enter a valid number, e.g., "118.61421", or range, e.g., "80 90". You can filter the columns by entering values and then click the "Filter" button.'

        if request.args.get('locus_dec'):
            dec_input = extract_numbers(request.args.get('locus_dec'))
            if dec_input != None:
                query = extract_float_filter(dec_input, Ztf.locus_dec, query)
            else:
                filter_warning_message += 'Dec filter cannot be applied - Enter a valid number, e.g., "-20.02131", or range, e.g., "18.8 19.4". You can filter the columns by entering values and then click the "Filter" button.'

        #if request.args.get('magpsf'):
            #magpsf_input = extract_numbers(request.args.get('magpsf'))
            #if magpsf_input != None:
                #query = extract_float_filter(magpsf_input, Ztf.magpsf, query)
            #else:
                #filter_warning_message += 'Magpsf filter cannot be applied - Enter a valid number, e.g., "18.84", or range, e.g., "18.8 19.4". You can filter the columns by entering values and then click the "Filter" button.'

        #Sort order by date (still sorts by mjd column)
        if request.args.get('sort__date'):
            sort__date_order = request.args.get('sort__date')
            if sort__date_order == 'desc':
                query = query.order_by(Ztf.date_alert_mjd.desc())
            if sort__date_order == 'asc':
                query = query.order_by(Ztf.date_alert_mjd.asc())

        #Sort order by candid
        if request.args.get('sort__candid'):
            sort__candid_order = request.args.get('sort__candid')
            if sort__candid_order == 'desc':
                query = query.order_by(Ztf.alert_id.desc())
            if sort__candid_order == 'asc':
                query = query.order_by(Ztf.alert_id.asc())
        
        #Sort order by objectId
        if request.args.get('sort__objectId'):
            sort__objectId_order = request.args.get('sort__objectId')
            if sort__objectId_order == 'desc':
                query = query.order_by(Ztf.ztf_object_id.desc())
            if sort__objectId_order == 'asc':
                query = query.order_by(Ztf.ztf_object_id.asc())

        #Sort order by jd
        #if request.args.get('sort__jd'):
            #sort__jd_order = request.args.get('sort__jd')
            #if sort__jd_order == 'desc':
                #query = query.order_by(Ztf.jd.desc())
            #if sort__jd_order == 'asc':
                #query = query.order_by(Ztf.jd.asc())

        #Sort order by ra
        if request.args.get('sort__ra'):
            sort__ra_order = request.args.get('sort__ra')
            if sort__ra_order == 'desc':
                query = query.order_by(Ztf.locus_ra.desc())
            if sort__ra_order == 'asc':
                query = query.order_by(Ztf.locus_ra.asc())

        #Sort order by dec
        if request.args.get('sort__dec'):
            sort__dec_order = request.args.get('sort__dec')
            if sort__dec_order == 'desc':
                query = query.order_by(Ztf.locus_dec.desc())
            if sort__dec_order == 'asc':
                query = query.order_by(Ztf.locus_dec.asc())

        ##Sort order by magpsf
        #if request.args.get('sort__magpsf'):
            #sort__magpsf_order = request.args.get('sort__magpsf')
            #if sort__magpsf_order == 'desc':
                #query = query.order_by(Ztf.magpsf.desc())
            #if sort__magpsf_order == 'asc':
                #query = query.order_by(Ztf.magpsf.asc())


        #latest = db.session.query(Ztf).order_by(Ztf.jd.desc()).first() # ? to show latest update date
        paginator = query.paginate(page, 100, True)
        #pdb.set_trace()
        # response = {
        #     'has_next': paginator.has_next,
        #     'has_prev': paginator.has_prev,
        #     'results': Alert.serialize_list(paginator.items)
        # }
        #pdb.set_trace()
        print(request.query_string.decode('ascii'))
        print(re.sub('[&?]page=\\d+', '', request.query_string.decode('ascii')))

    return render_template(
        "main.html",
        total_queries=paginator.total,
        table=paginator.items,
        page=paginator.page,
        has_next=paginator.has_next,
        last_page=paginator.pages,
        query_string=re.sub('[&?]?page=\\d+', '', request.query_string.decode('ascii')), # ? b'' binary string
        filter_warning = filter_warning_message
    )

@app.route('/query_lightcurve_data', methods=['GET'])
def query_lightcurve_data():
    locusId = request.args.get('locusId')

    #query where locus id equals selected id
    lightcurve_query = db.session.query(Ztf)
    lightcurve_query = lightcurve_query.filter(Ztf.locus_id == locusId) #TODO: load only specific columns
    data = lightcurve_query.all()
    #fields = ['id', 'date_alert_mjd', 'ant_mag_corrected']
    #data = lightcurve_query.options(db.load_only(Ztf.id, Ztf.date_alert_mjd, Ztf.ant_mag_corrected)).all()

    # Creating Plot Figure
    p = figure(height=350, sizing_mode="stretch_width") 
    p.xaxis.axis_label = 'date_alert_mjd'
    p.yaxis.axis_label = 'ant_mag_corrected'
    
    # Defining Plot to be a Scatter Plot
    x_coords = []
    y_coords = []
    #prepare x and y coordinates of rows matched by locus_id of the g band
    for row in (item for item in data if item.ant_passband == 'i'):
        if (row.date_alert_mjd != None and row.ant_mag_corrected != None):
            x_coords += [row.date_alert_mjd]
            y_coords += [row.ant_mag_corrected]
    p.scatter(
        # [i for i in range(10)],
        # [random.randint(1, 50) for j in range(10)],
        x_coords,
        y_coords,
        size=5,
        color="darkkhaki",
        alpha=0.5
    )
    x_coords = []
    y_coords = []
    #prepare x and y coordinates of rows matched by locus_id of the g band
    for row in (item for item in data if item.ant_passband == 'R'):
        if (row.date_alert_mjd != None and row.ant_mag_corrected != None):
            x_coords += [row.date_alert_mjd]
            y_coords += [row.ant_mag_corrected]
    p.scatter(
        # [i for i in range(10)],
        # [random.randint(1, 50) for j in range(10)],
        x_coords,
        y_coords,
        size=5,
        color="indianred",
        alpha=0.5
    )
    x_coords = []
    y_coords = []
    #prepare x and y coordinates of rows matched by locus_id of the g band
    for row in (item for item in data if item.ant_passband == 'g'):
        if (row.date_alert_mjd != None and row.ant_mag_corrected != None):
            x_coords += [row.date_alert_mjd]
            y_coords += [row.ant_mag_corrected]
    p.scatter(
        # [i for i in range(10)],
        # [random.randint(1, 50) for j in range(10)],
        x_coords,
        y_coords,
        size=5,
        color="limegreen",
        alpha=0.5
    )
 
    # Get Chart Components
    script, div = components(p)
 
    # Return the components to the HTML template
    return f'{ div }{ script }'

    return f'''
    <html lang="en">
        <head>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-2.3.3.min.js"></script>
            <title>Bokeh Charts</title>
        </head>
        <body>
            <h1>Add Graphs to Flask apps using Python library - Bokeh</h1>
            { div }
            { script }
        </body>
    </html>
    '''

@app.route("/locus_plot_csv")
def get_locus_plot():
    locusId = request.args.get('locusId')
    #query where locus id equals selected id
    lightcurve_query = db.session.query(Ztf)
    lightcurve_query = lightcurve_query.filter(Ztf.locus_id == locusId) #TODO: load only specific columns
    data = lightcurve_query.all()
    csv = 'locus_id,date_alert_mjd,ant_mag_corrected\n'
    #prepare x and y coordinates of rows matched by locus_id
    for row in data:
        if (row.date_alert_mjd != None and row.ant_mag_corrected != None):
            csv += f'{row.locus_id},{row.date_alert_mjd},{row.ant_mag_corrected}\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})



# import pandas as pd
# from pathlib import Path
# @app.route('/generate_lightcurve', methods=['GET'])
# def generate_lightcurve():
#     #objectId = request.args.get('objectId')
#     objectId = request.args.get('ztf_object_id')
#     print('objectId: ', objectId)
#     #generate lightcurve, store it on the server
#     my_file = Path('static/_ZTF_lightcurves_concat/'+objectId+'.csv')
#     lc_plot_uri = '/static/img/_ZTF_lc_plots/'+objectId+'.png' #expected result path
#     if my_file.is_file():
#         df = pd.read_csv(my_file)
#         foldername = Path("static/img/_ZTF_lc_plots")
        
#         dflc = generate_dcmag_lightcurve(df)
#         lc_plot_uri = plot_lightcurve(dflc, foldername, objectId)
#     else:
#         lc_plot_uri = '/static/img/_ZTF_lc_plots/missing_file.png' #missing CSV #TODO: This shoud work now as handled in JS CsvExists(), TEST!
#     #print('/static/img/_ZTF_lc_plots/'+objectId+'.png')
#     print(lc_plot_uri)
#     response = make_response(lc_plot_uri, 200)
#     response.mimetype = "text/plain"
#     return response


#NOTE: Features are filter by objectId & candid
@app.route('/query_features', methods=['GET'])
def query_features():
    #objectId = request.args.get('objectId')
    #objectId = request.args.get('ztf_object_id')
    #candid = request.args.get('candid')
    alert_id = request.args.get('alert_id')
    #print('objectId: %s; candid: %s' % ('', alert_id))

    feature_query = db.session.query(Ztf)
    #feature_query = feature_query.filter(Ztf.objectId == objectId)
    feature_query = feature_query.filter(Ztf.alert_id == 'ztf_candidate:'+alert_id)
    data = object_as_dict(feature_query.first())
    #print(data)
    
    response = app.response_class(
        response=json.dumps(data), #TODO? array[] with single row when using BootstrapTable?
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/query_featureplot_data', methods=['GET'])
def query_featureplot_data():
    locusId = request.args.get('locusId')
    selected_features = request.args.get('features')
    #default selected feature list
    feature_list = ['feature_amplitude_magn_r',
        'feature_anderson_darling_normal_magn_r',
        'feature_beyond_1_std_magn_r',
        'feature_beyond_2_std_magn_r',
        'feature_cusum_magn_r']

    if selected_features:
        features_array = selected_features.split(',')
        if features_array and len(features_array) > 0:
            feature_list = features_array
            #print(feature_list)

    #query where locus id equals selected id
    featureplot_query = db.session.query(Ztf)
    featureplot_query = featureplot_query.filter(Ztf.locus_id == locusId) #TODO: load only specific columns
    data = featureplot_query.all()
    #fields = ['id', 'date_alert_mjd', 'ant_mag_corrected']
    #data = lightcurve_query.options(db.load_only(Ztf.id, Ztf.date_alert_mjd, Ztf.ant_mag_corrected)).all()

    # Creating Plot Figure
    p = figure(height=350, sizing_mode="stretch_width") 
    p.xaxis.axis_label = 'date_alert_mjd'
    p.yaxis.axis_label = 'features'
    # Defining Plot to be a Scatter Plot
    x_coords = []
    y_coords = []
    #TODO Features: Retrieve from args.get() - if none: select these as defaults

    #10! colors
    data_colors = [
        "#1f77b4",  # blue
        "#ff7f0e",  # orange
        "#2ca02c",  # green
        "#d62728",  # red
        "#9467bd",  # purple
        "#8c564b",  # brown
        "#e377c2",  # pink
        "#7f7f7f",  # gray
        "#bcbd22",  # yellow-green
        "#17becf"   # cyan
    ]
    #prepare x and y coordinates of rows matched by locus_id
    legend_it = []
    for index, feature in enumerate(feature_list):
        x_coords = []
        y_coords = []
        for row in data:
            if (row.date_alert_mjd != None and row.ant_mag_corrected != None):
                x_coords += [row.date_alert_mjd]
                value = getattr(row, feature)
                #print([getattr(row, feature)])
                y_coords += [value]
        print(x_coords)
        print(y_coords)
        pc = p.scatter(
            # [i for i in range(10)],
            # [random.randint(1, 50) for j in range(10)],
            x_coords,
            y_coords,
            size=5,
            color=data_colors[index],
            alpha=0.5
            #,legend_label=feature
        )
        legend_it.append((feature, [pc]))

    legend = Legend(items=legend_it)  #, glyph_height=9, glyph_width=9)
    #legend.click_policy="mute"
    
    # Increasing the glyph height
    # p.legend.glyph_height = 5    
    # # increasing the glyph width
    # p.legend.glyph_width = 5   
    # # Increasing the glyph's label height
    # p.legend.label_height = 5 
    # # Increasing the glyph's label height
    # p.legend.text_font_size = '6px'
    p.add_layout(legend, 'right')
    p.legend.label_text_font_size = '9px'
    p.legend.glyph_width = 12
 
    # Get Chart Components
    script, div = components(p)
    print(div)
 
    # Return the components to the HTML template
    return f'{ div }{ script }'


#NOTE: #classification filter by objectId
@app.route('/query_classification', methods=['GET'])
def query_classification():
    #objectId = request.args.get('objectId')
    objectId = request.args.get('ztf_object_id')
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

if __name__ == '__main__':
    app.run(debug=True) #uses flask debugger
#    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True) #disable flask debuger and use external debugger instead

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
        print(input_field[0])
        print(input_field[1])
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
