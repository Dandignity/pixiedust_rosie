import classify_data as cd
import pixiedust
from pixiedust.display.app import *
from pixiedust.utils.shellAccess import ShellAccess

@PixieApp
class PixieRosieApp:

    def textToInt(self,text):
        return int(text)

    @route()
    def main(self):
        return"""
            <div id=target{{prefix}} class="well">
                <div class="panel panel-primary">
                    <div class="panel-heading">Schema</div>
                    <div class="panel-body">
                        <table class="table table-bordered table-striped">
                            <thead>
                                <th>Column Name</th>
                                <th>Rosie Type</th>
                                <th>Column Type</th>
                                <th>Action</th>
                            </thead>
                            {%for display, name, rosie_type, native_type in this.schema.create_schema_table():%}
                                {% if display %}
                                    <tr>
                                        <td>{{name}}</td>
                                        <td>{{rosie_type}}</td>
                                        <td>{{native_type.__name__}}</td>
                                        <td>
                                            <button type="submit" pd_options="modify={{loop.index0}}">Rename</button>
                                            <button type="submit" pd_script="self.schema.create_transform({{loop.index0}})" pd_options="transform={{loop.index0}}">Transform</button>
                                            <button type="submit" pd_refresh>Delete
                                                <pd_script type="preRun">
                                                    return confirm("Are you sure you want to delete?");
                                                </pd_script>
                                                <pd_script>
                                                    self.schema.hide_column({{loop.index0}});
                                                </pd_script>
                                            </button>
                                        </td>
                                    </tr>
                                {% endif %}
                            {%endfor%}
                        </table>
                    </div>
                    </div>
                    <br/>
                    <div class="panel panel-primary">
                        <div class="panel-heading">Sample Data</div>
                        <div class="panel-body">
                            <table class="table table-bordered table-striped">
                                <thead>
                                    {%for name in this.schema.colnames:%}
                                        {% if this.schema.column_visibility[loop.index0] %}
                                            <th>{{name}}</th>
                                        {% endif %}
                                    {%endfor%}
                                </thead>
                                {%for row in this.schema.sample_data:%}
                                    <tr>
                                    {%for col in row:%}
                                        {% if this.schema.column_visibility[loop.index0] %}
                                            <td>{{col}}</td>
                                        {% endif %}
                                    {%endfor%}
                                    </tr>
                                {%endfor%}
                            </table>
                        </div>
                    </div>
                    <input pd_options="RosieUI=true" type="button" value="Finish">
                </div>
            """

    @route(modify="*")
    def modify_screen(self, modify):
        return """
        <div class="well">
            <form>
                <div>
                    <input type="search" id="new_name{{prefix}}" name="colname" placeholder="new name...">
                    <br/>
                    <br/>
                    <input pd_options="home=true" type="button" value="Cancel">
                    <button type="submit" pd_script="self.schema.rename_column({{modify}}, '$val(new_name{{prefix}})')" pd_options="home=true">Rename</button>
                </div>
            </form>
        </div>
        """

    @route(transform="*")
    def transform_screen(self, transform):
        return """
        <div class="well">
            <div class="panel panel-primary">
                <div class="panel-heading">Pattern</div>
                <div class="panel-body">
                    <style>
                        p {
                          text-indent: 4.0em;
                        }
                    </style>
                   <div class="search">
                        Pattern: <br/>
                        <input type="text" id="pat{{prefix}}" class="searchTerm" placeholder="{{this.schema.transform.pattern}}">
                        <button type="submit" pd_script="self.schema.transform.extract_components('$val(pat{{prefix}})')" pd_options="transform={{transform}}">Define</button>
                   </div>
                   {% if this.schema.transform.components %}
                        {%for comp in this.schema.transform.components:%}
                            <p>
                                <input type="text" id="comp1{{prefix}}" class="searchTerm" value="{{comp.name}}" readonly>
                                <input type="text" id="comp2{{prefix}}" class="searchTerm" placeholder="definition">
                            </p>
                        {%endfor%}
                        <br>
                        <button type="submit" pd_script="self.schema.transform.create_sample_data()" pd_options="transform={{transform}}">Run</button>
                   {% endif %}
                </div>
            </div>
            <br/>
            <div class="panel panel-primary">
                <div class="panel-heading">Selected Column</div>
                <div class="panel-body">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <th style="text-align: left;">{{this.schema.colnames[this.textToInt(transform)]}}</th>
                        </thead>
                        {%for row in this.schema.sample_data:%}
                            <tr>
                            {%for col in row:%}
                                {% if loop.index0 == this.textToInt(transform) %}
                                    <td style="text-align: left;">{{col}}</td>
                                {% endif %}
                            {%endfor%}
                            </tr>
                        {%endfor%}
                    </table>
                </div>
            </div>
            <br />
            <div class="panel panel-primary">
                <div class="panel-heading">New Column(s)</div>
                <div class="panel-body">
                    <table class="table table-bordered table-striped">
                        {% if this.schema.transform.new_col_names %}
                            <thead>
                                {%for name in this.schema.transform.new_col_names:%}
                                    <th>{{name}}</th>
                                {%endfor%}
                            </thead>
                            {%for row in this.schema.transform.preview:%}
                                <tr>
                                {%for col in row:%}
                                    <td>{{col}}</td>
                                {%endfor%}
                                </tr>
                            {%endfor%}
                        {% endif %}
                    </table>
                </div>
            </div>
            <input pd_options="home=true" type="button" value="Cancel">
            <button type="submit" pd_script="" pd_options="home=true"" >Create Columns</button>
        </div>
        """