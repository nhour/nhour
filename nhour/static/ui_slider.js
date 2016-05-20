function createSlider(start) {
    var slider = document.getElementById('slider');
    var selectedHours = document.getElementById('hours-selected');
    var hours = document.getElementById('id_hours')

    noUiSlider.create(slider, {
        start: start,
        behaviour: 'tap',
        connect: 'lower',
        range: {
            'min':  0.5,
            'max':  40
        },
        step: 0.5,
    });

    slider.noUiSlider.on('update', function(values, handle) {
        hours.value = values[handle];
        selectedHours.value = values[handle];
    });

    $(selectedHours).change(function(event) {
        newHours = $(event.target).val()
        slider.noUiSlider.set(newHours);
    });
}