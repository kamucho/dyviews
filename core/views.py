import ast
import subprocess
import sys

from django.shortcuts import render, redirect

from core.models import Function

__all__ = [
    'add',
    'delete',
    'edit',
    'exec_func',
    'home',
]


def home(request):
    functions = Function.objects.all()
    return render(request, 'all.html', {'functions': functions})


def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        params_count = int(request.POST.get('params-count'))
        code = request.POST.get('code')
        params = {}
        for i in range(params_count):
            params[request.POST.get(f'param-{i + 1}')] = request.POST.get(f'param-type-{i + 1}')
        function = Function(name=name, code=code, params=str(params))
        function.save()
        for dependency in request.POST.get('dependencies').split(','):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
        return redirect('home')


def delete(request, pk):
    Function.objects.filter(pk=pk).delete()
    return redirect('home')


def edit(request, pk):
    if request.method == 'GET':
        function = Function.objects.get(pk=pk)
        params = ast.literal_eval(function.params)
        return render(request, 'edit.html', {'function': function, 'params': params})
    elif request.method == 'POST':
        function = Function.objects.get(pk=pk)
        function.name = request.POST.get('name')
        function.code = request.POST.get('code')
        function.save()
        return redirect('home')


def exec_func(request, pk):
    if request.method == 'GET':
        function = Function.objects.get(pk=pk)
        params = ast.literal_eval(function.params)
        return render(request, 'get_params.html', {'params': params, 'id': pk, 'code': function.code})

    if request.method == 'POST':
        function = Function.objects.get(pk=pk)
        params = ast.literal_eval(function.params)
        code = ''
        for i in params.keys():
            if params[i] != 'str':
                code += f'{i}={ast.literal_eval(request.POST.get(i))}\n'
            else:
                code += f'{i}="{request.POST.get(i)}"\n'
        code += function.code
        code = code.replace('\n', '\n    ')
        loc = {}
        exec(f'def dynamic_func():\n    {code}', globals(), loc)
        output = loc['dynamic_func']()
        return render(request, 'output.html', {'output': output})
