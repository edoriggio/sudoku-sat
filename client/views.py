from django.shortcuts import render
from django.views import View

from .src.sudoku import solve


class Home(View):
    _context = {}

    def get(self, request):
        self._context = {'sol_matrix': solve()}

        return render(request, 'home.html', context=self._context)
