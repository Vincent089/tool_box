import csv
import plotly.graph_objs as go


class Graph(object):

    def __init__(self, x_data, y_data, y_label, graph_title):
        self._fig = go.Figure()
        self._data = y_data
        self._x = x_data

        # build graph inner figure
        self._build_figure(fig_title=graph_title,
                           xaxis_title='Date',
                           yaxis_title=y_label)

    def render_to_json_data(self):
        return self._fig.to_json()

    def render(self):
        self._fig.show()

    def _build_figure(self, fig_title, xaxis_title, yaxis_title):
        line_colors= ['#b33655', '#F2A200', '#66c0ff', '#6ba1b3', '#007535', '#E31937', '#505659']

        self._fig.update_layout(title=fig_title,
                                yaxis_title=yaxis_title,
                                xaxis_title=xaxis_title,
                                plot_bgcolor='#f2f2f2',
                                colorway=line_colors)

        for datacenter_key, datacenter_value in self._data.items():
            for plateforme_key, plateforme_value in self._data.get(datacenter_key).items():
                # create a label for the Y Axe
                label = '%s %s' % (plateforme_key, datacenter_key)

                if plateforme_key == 'CONNECT':
                    self._add_trace(label, plateforme_value)

                if plateforme_key == 'RNAS':
                    self._add_trace(label, plateforme_value, 'dash')

                if plateforme_key == 'LITE':
                    self._add_trace(label, plateforme_value, 'dot')

    def _add_trace(self, trace_label, trace_data, trace_style=None):
        '''
        Create and style traces
        :param trace_label:
        :param trace_data:
        :return:
        '''

        self._fig.add_trace(go.Scatter(x=self._x,
                                       y=trace_data,
                                       name=trace_label,
                                       line=dict(width=4, dash=trace_style)))


def get_data_for_graph_xaxis(key, data_list):
    '''
    Extract a specific jkey from the data_list and retunr and array of unique values to be use in Graph as xaxis
    :param key:
    :param data_list:
    :return:
    '''
    data = []

    for row in data_list:
        if row[key] not in data:
            data.append(row[key])

    return data


def get_data_for_graph_yaxis(key, data_list):
    '''
    Extract a specific key from the data_list and return a formatted dict to be use in Graph as yaxis
    :param key:
    :param data_list:
    :return:
    '''
    data = {}

    # loop over all row and extract specific key
    for row in data_list:
        if row['Datacenter'] not in data:
            data[row['Datacenter']] = {}

        if row['Plateforme'] not in data[row['Datacenter']]:
            # create the frame list for the datacenter equal to the length of hit dates
            data[row['Datacenter']][row['Plateforme']] = [None] * len(hits_date)

        # update the index value of the list at the same index as the hit date
        date_index = hits_date.index(row['date'])
        data[row['Datacenter']][row['Plateforme']].insert(date_index, row[key])

    return data


def generate_html_report(json_data):
    template = """
    <!doctype html>
    <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            
            <!-- Bootstrap 4 style -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
            
            <!-- Rendering script for Plotly -->
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            
            <title>UA Stats Report</title>
        </head>
        <body>
            <!-- Navigation -->
            <header class="navbar navbar-expand-lg navbar-light bg-light shadow fixed-top" style="border-top: 4px solid #991F3D">
              <div class="container">              
                <a class="navbar-brand" href="#" style="color:#991F3D">
                    <img width="53" height="33" src="../static/cgi_black.png">
                    <span class="align-middle">Unify Access Utilisation Report</span>
                </a>
                
                <!-- Uncomment if needs to have mutiple nav destination
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="navbarResponsive">
                  <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                      <a class="nav-link" href="#">Home
                        <span class="sr-only">(current)</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="#">About</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="#">Services</a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" href="#">Contact</a>
                    </li>
                  </ul>
                </div>
                -->
                
              </div>
            </header>
            
            <div class="container" style="margin-top:5%">
                <div class="row">
                    <div class="col-12">
                        <div id='divUserLoadPlotly'></div>
                        <div id='divCPUPlotly'></div>
                        <div id='divMemPlotly'></div>
                    </div>
                </div>
                
            </div>
            
            <footer class="navbar navbar-expand-lg navbar-light border-top" style="background-color: #e4e8eb; height: 48px">
                <div class="container">
                    <span class="text-left align-middle">CGI - Internal Use Only</span>
                    <img class="float-right" style="height:33px; width:53px" src="../static/cgi_cherry.png">                    
                </div>
            </footer>
            
            <!-- Bootstrap 4 scripts -->
            <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
            
            <!-- Plotly script to create graph -->
            <script>
                const user_load_data = {}
                const cpu_usage_data = {}
                const mem_usage_data = {}
                
                Plotly.react('divUserLoadPlotly', user_load_data.data, user_load_data.layout);
                Plotly.react('divCPUPlotly', cpu_usage_data.data, cpu_usage_data.layout);
                Plotly.react('divMemPlotly', mem_usage_data.data, mem_usage_data.layout);
            </script>
        </body>
        </html>"""

    # write the JSON to the HTML template
    with open(report_folder, 'w') as f:
        f.write(template.format(json_data['user_load_data'],
                                json_data['cpu_usage_data'],
                                json_data['mem_usage_data']))


# Entry point
if __name__ == "__main__":

    # local device path
    # data_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_input\ua_stats.csv'
    # report_folder = r'../_file_output/report_plot.html'

    # prod path
    data_location = r'/u/data/nginx/ua_stats.csv'
    report_folder = r'/u/data/nginx/html/ua_report.html'

    # read data csv and format various object to be use uin Graph
    with open(data_location, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        csv_data = list(csv_reader)

    hits_date = get_data_for_graph_xaxis('date', csv_data)
    nb_user_data = get_data_for_graph_yaxis('NbUserConnected', csv_data)
    cpu_usage_data = get_data_for_graph_yaxis('CPU', csv_data)
    mem_usage_data = get_data_for_graph_yaxis('Memory', csv_data)

    # create graph
    user_load_graph = Graph(x_data=hits_date, y_data=nb_user_data,
                            y_label='Number of users', graph_title='UA plateforme, User connected by datacenter')
    cpu_graph = Graph(x_data=hits_date, y_data=cpu_usage_data,
                      y_label='CPU usage (%)', graph_title='UA plateforme, CPU usage by datacenter')
    mem_graph = Graph(x_data=hits_date, y_data=mem_usage_data,
                      y_label='Memory utilisation', graph_title='UA plateforme, Memory utilisation by datacenter')

    # render graph as json data
    user_load_graph_json = user_load_graph.render_to_json_data()
    cpu_graph_json = cpu_graph.render_to_json_data()
    mem_graph_json = mem_graph.render_to_json_data()

    # render to single page output
    # user_load_graph.render()
    # cpu_graph.render()
    # mem_graph.render()

    data = {
        'user_load_data': user_load_graph_json,
        'cpu_usage_data': cpu_graph_json,
        'mem_usage_data': mem_graph_json
    }

    generate_html_report(data)
