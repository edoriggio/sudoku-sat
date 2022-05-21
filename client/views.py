from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from .src.sudoku import solve, check_solution


class Home(View):
    _context = {}

    def get(self, request):
        self._context = {'sol_matrix': [' '*9]*9}

        return render(request, 'home.html', context=self._context)


class Solve(View):
    def post(self, request):
        content = request.body.decode('utf-8')

        return JsonResponse({'sol_matrix': solve(content)})


class Check(View):
    def post(self, request):
        content = request.body.decode('utf-8')

        return JsonResponse({'check': check_solution(content)})
