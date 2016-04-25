function createSlider(start) {
    var slider = document.getElementById('slider');
    var selectedHours = document.getElementById('hours-selected');

    noUiSlider.create(slider, {
        start: start,
        behaviour: 'tap',
        connect: 'lower',
        range: {
            'min':  0.5,
            'max':  50
        },
        step: 0.5,
    });
    slider.noUiSlider.on('update', function(values, handle) {
        selectedHours.textContent = values[handle]
        hours.value = values[handle]
    });
}