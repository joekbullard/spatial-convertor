from django.views.generic import TemplateView
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.core.files.uploadedfile import TemporaryUploadedFile
import zipfile
from pathlib import Path
from .convertor import convertor
import fiona
from fiona.io import ZipMemoryFile
import geopandas as gpd
import tempfile
import os
import codecs
import shutil

class HomeView(TemplateView):
    template_name = "home.html"


"""
def extract_zip_file(zip_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for path in temp_dir.glob('./*'):
            if Path(path).suffix == ".shp":
                temp_file = tempfile.NamedTemporaryFile(prefix='my_temp_file_', delete=False)
                processed_file = convertor(path, temp_file.name, 'GPKG')

        
        response = FileResponse(processed_file, content_type='application/octet-stream')


        response['Content-Disposition'] = 'attachment; filename="processed_file.txt"'

"""


import io

import fiona.io

def file_upload_view(request):
    if request.method == "POST" and request.FILES:
        uploaded_file = request.FILES["file"]

        with fiona.io.MemoryFile(uploaded_file, ext='gpkg') as src_memfile:
            layers = src_memfile.listlayers()
            for layername in layers:
                with src_memfile.open() as src:

                    out_crs = src.crs
                    out_encoding = src.encoding
                    out_schema = src.schema

                    in_memory_zip = io.BytesIO()


                    with fiona.io.MemoryFile() as out_memfile:
                        with out_memfile.open(
                            mode="w",
                            crs=src.crs,
                            driver="GPKG",
                            schema=out_schema,
                            encoding = out_encoding
                        ) as out:
                            out.writerecords(src)

                            with zipfile.ZipFile(in_memory_zip, 'w') as zipf:
                                zipf.writestr('output.zip', out_memfile.read())

                    in_memory_zip.seek(0)

                    # Create a Django HttpResponse with the in-memory ZIP file as content
                    response = HttpResponse(in_memory_zip, content_type='application/force-download')

                    # Set the appropriate headers for the ZIP download
                    response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'

                    # Return the response
                    return response




                    # with tempfile.TemporaryDirectory() as temp_dir:
                    #     temp_dir = Path(temp_dir)
                    #     filename = 'output.gpkg'
                    #     fullpath = temp_dir / filename

                    #     gdf.to_file(filename=fullpath, driver='GPKG', encoding='utf-8')

                    #     with open(fullpath, "rb") as fh:
                    #         response = HttpResponse(fh, content_type="application/force-download")
                    #         response['Content-Disposition'] = 'inline; filename=output.gpkg'
                    #         return response


        ''''

        for layer in layers:
            print(layer)
            gdf = gpd.read_file(in_memory_file, layer=layer)

            with io.BytesIO() as tmp_zip_obj:
                gdf.to_file(tmp_zip_obj, driver='GPKG', encoding='utf-8')
                tmp_zip_file_name = 'output.zip'

                with zipfile.ZipFile(tmp_zip_obj, 'w') as zip_file:
                    for file in zip_file.filelist:
                        if file.filename != tmp_zip_file_name:
                            zip_file.extract(file, tmp_zip_obj)

                tmp_zip_obj.seek(0)

                with open('output.zip', 'rb') as file:
                    response = HttpResponse(file, content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=output.zip'
                    print('success')
                    return response



        # check if zipfile (for shapefile)
        # what behaviour do we want?
        # First - check if zipfile - if it is return layers included
        # with open(path_like_object, "rb") as f:
        #     layers = fiona.listlayers(f.name)
            
        #     response = HttpResponse(content_type='application/zip')
        #     zf = zipfile.ZipFile(response, 'w')
        #     zf.write(path_like_object, 'w')
        #     response['Content-Disposition'] = 'attachment; filename=test.zip'
        #     return response
        '''
        '''
        else:
            try:
                layers = fiona.listlayers(path_like_object)
            except:
                pass

        html = ""

        for layer in layers:
            print(layer)
            html = html + f"<p>{layer}</p>\n"

        print(html)

        return HttpResponse(html)
        '''
        """

        with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_ref.extractall(temp_dir)

                temp_path = Path(temp_dir)

                for file_path in temp_path.glob("**/*.shp"):
                    input_shp = temp_path / file_path

                    with fiona.open(input_shp, "r") as src:
                        output_schema = src.schema

                        with tempfile.TemporaryDirectory() as temp_out_dir:
                            temp_output_file = temp_out_dir + "/output.gpkg"

                            with fiona.open(
                                temp_output_file,
                                mode="w",
                                crs=src.crs,
                                driver="GPKG",
                                schema=output_schema,
                            ) as dst:
                                for feat in src:
                                    dst.write(feat)

                                # processed_file = convertor(input_shp, temp_output_file_path, 'GPKG')


                                with open(temp_output_file, "rb") as fh:
                                    response = HttpResponse(fh.read(), content_type="application/force-download")
                                    response['Content-Disposition'] = 'inline; filename=' + f'output.gpkg'
                                    return response
                        
        # layers = fiona.listlayers(uploaded_file)
        # list = [layer for layer in layers]

        
    # HttpResponse("\n".join(layers))

    return render(request, "home.html")
"""
