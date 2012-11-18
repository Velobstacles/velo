<%inherit file="base.mako"/>


<form id="media" class="form-horizontal" action="${request.rest_resource_url('medium')}" enctype="multipart/form-data" method="post">
  <fieldset>
    <legend>Create Medium</legend>

    <div class="control-group">
      <label class="control-label" for="latitude">Latitude</label>
      <div class="controls">
        <input type="text" name="latitude" placeholder="Latitude">
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="longitude">Longitude</label>
      <div class="controls">
        <input type="text" name="longitude" placeholder="Longitude">
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="source">File</label>
      <div class="controls">
        <input type="file" name="source"></input>
      </div>
    </div>
    <div class="control-group">
      <div class="controls">
        <input type="submit" class="btn" value="Create"/>
      </div>
    </div>

</form>
