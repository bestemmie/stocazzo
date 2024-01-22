from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm
import os, random, string, time, shutil, re
from .forms import bestClickerForm

def homepage(request):
    return render(request, "homepage.html")

def trucchi(request):
    return render(request, "trucchi.html")

def ss(request):
    return render(request, "ss.html")

def staff(request):
    return render(request, "staff.html")

def best_buildform(request):
    form = bestClickerForm()
    return render(request, "generator.html", {'form':form})

def best_download(request):
    if (request.method == "POST"):
        form = bestClickerForm(request.POST)

        if (form.is_valid()):

            # Vars

            name = "temp-"
            dll_name = form.cleaned_data["dll_name"]
            exe_name = form.cleaned_data["exe_name"]

            root = "/var/www/stocazzo"

            for i in range(10):
                name += str(random.choice(string.ascii_lowercase))

            # Regex

            if not (re.fullmatch("^[a-zA-Z0-9]*$",dll_name)):
                return HttpResponse("Coglione non puoi !!!!!")

            if not (re.fullmatch("^[a-zA-Z0-9]*$",exe_name)):
                return HttpResponse("Coglione non puoi !!!!!")

            # Try

            check = 0

            try:

                # Make a directory

                if (os.name == 'nt'):
                    pass
                else:
                    os.system("cd")
                    os.system(f"cd {root}/main/bestclicker/build && mkdir {name} && cd {name} && mkdir bestclicker")
                    check += 1

                # Copy files

                if (os.name == 'nt'):
                    os.system(f"copy .\\main\\bestclicker\\src\\main.cpp .\\main\\bestclicker\\build\\{name}\\main.cpp")
                    os.system(f"copy .\\main\\bestclicker\\src\\main.dll .\\main\\bestclicker\\build\\{name}\\bestclicker\\{dll_name}.dll")
                    os.system(f"copy .\\main\\bestclicker\\src\\boot.vbs .\\main\\bestclicker\\build\\{name}\\bestclicker\\boot.vbs")
                else:
                    os.system(f"cp {root}/main/bestclicker/src/main.cpp {root}/main/bestclicker/build/{name}/main.cpp")
                    check += 1
                    os.system(f"cp {root}/main/bestclicker/src/main.dll {root}/main/bestclicker/build/{name}/bestclicker/{dll_name}.dll")
                    check += 1
                    os.system(f"cp {root}/main/bestclicker/src/boot.vbs {root}/main/bestclicker/build/{name}/bestclicker/boot.vbs")
                    check += 1

                # Edit files

                with open(f"{root}/main/bestclicker/build/{name}/main.cpp", 'r+') as f:
                    # read a list of lines into data
                    data = f.readlines()
                    f.close()

                check += 1

                data[12] = f'char* dll_path = "{dll_name}.dll";'

                with open(f"{root}/main/bestclicker/build/{name}/main.cpp", 'w+') as f:
                    f.writelines(data)
                    f.close()

                check += 1

                # Build
                if (os.name == 'nt'):
                    os.system(
                        f"g++.exe -Wall -fexceptions -O2  -c ./main/bestclicker/build/{name}/main.cpp -o ./main/bestclicker/build/{name}/main.o")
                    os.system(
                        f"g++.exe  -o ./main/bestclicker/build/{name}/bestclicker/{exe_name}.exe ./main/bestclicker/build/{name}/main.o  -s  ./main/bestclicker/src/libws2_32.a")
                else:
                    os.system(
                        f"x86_64-w64-mingw32-g++ -Wall -fexceptions -O2  -c {root}/main/bestclicker/build/{name}/main.cpp -o {root}/main/bestclicker/build/{name}/main.o")
                    check += 1
                    os.system(
                        f"x86_64-w64-mingw32-g++ -static-libgcc -static-libstdc++ -static -pthread -o {root}/main/bestclicker/build/{name}/bestclicker/{exe_name}.exe {root}/main/bestclicker/build/{name}/main.o  -s  {root}/main/bestclicker/src/libws2_32.a")

                check += 1

                # Zip

                if (os.name == 'nt'):
                    os.system(f"7z a -tzip ./main/static/files/{name}.zip ./main/bestclicker/build/{name}/bestclicker")
                    shutil.rmtree(".\\main\\bestclicker\\build\\" + name)
                else:
                    os.system(f"cd {root}/main/bestclicker/build/{name} && zip -r ../../../static/files/{name}.zip bestclicker")
                    print("zipped")
                    check += 1
                    shutil.rmtree(f"{root}/main/bestclicker/build/{name}")
                    print("deleted")
                    check += 1

                return render(request, "download.html", {'name':name})
            except Exception as e:
                return HttpResponse(f"This is the check ({check}) and error: {e}")

    else:
        return HttpResponse("Coglione non puoi !!!!!")



