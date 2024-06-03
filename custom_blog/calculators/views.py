from django.shortcuts import render, redirect
from .forms import MotoPriceForm, MarkForm
from .utils import price_model, age_counter, mean_vollume, mean_power


# Create your views here.
def choose_mark(request):
    form = MarkForm(request.GET or None)
    if form.is_valid():
        mark = form.cleaned_data['mark']
        return redirect('calculator:price', mark)
    context = {'form': form}
    return render(request, 'calculators/price.html', context)


def price_calculator(request, mark):
    form = MotoPriceForm(request.GET or None, mark = mark)
    context = {'form': form,
               'mark': mark.title()}
    
    if form.is_valid():
        age=age_counter(form.cleaned_data['year'])
        model=form.cleaned_data['model']
        
        if not form.cleaned_data['vollume']:
            vollume = mean_vollume(mark, model)
            print(vollume)
        else:
            vollume = form.cleaned_data['vollume']

        if not form.cleaned_data['power']:
            power = mean_power(mark, model)
        else:
            power = form.cleaned_data['power']
        example = [mark,
            form.cleaned_data['model'],
            vollume,
            power,
            form.cleaned_data['mileage'],
            age
            ]
        price = price_model(example)
        context.update({'price': price})
    return render(request, 'calculators/price.html', context)
