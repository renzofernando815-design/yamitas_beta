document.addEventListener('DOMContentLoaded', function () {
    const daysContainer = document.querySelector('.calendar-days');
    const monthLabel = document.querySelector('.calendar-header .month-label');
    const prevButton = document.querySelector('.calendar-header .prev-month');
    const nextButton = document.querySelector('.calendar-header .next-month');
    const eventList = document.querySelector('.event-list');
    const eventForm = document.querySelector('#event-form');
    const eventName = document.querySelector('#nombre');
    const eventDescription = document.querySelector('#descripcion');
    const eventDate = document.querySelector('#fecha');
    const eventLocation = document.querySelector('#ubicacion');
    const authNotice = document.querySelector('.auth-notice');

    const allEvents = JSON.parse(document.querySelector('#eventos-json').textContent || '[]');
    let currentDate = new Date();
    let selectedDate = null;

    function formatMonthYear(date) {
        return date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });
    }

    function buildCalendar(date) {
        daysContainer.innerHTML = '';
        const year = date.getFullYear();
        const month = date.getMonth();
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        monthLabel.textContent = formatMonthYear(date);

        const startDayIndex = (firstDay + 6) % 7;

        for (let i = 0; i < startDayIndex; i++) {
            const blankDay = document.createElement('div');
            blankDay.classList.add('calendar-day', 'empty');
            daysContainer.appendChild(blankDay);
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const button = document.createElement('button');
            button.type = 'button';
            button.classList.add('calendar-day');

            const dateValue = new Date(year, month, day);
            const isoDate = dateValue.toISOString().slice(0, 10);
            button.dataset.date = isoDate;
            button.textContent = day;

            const eventForDay = allEvents.filter(e => e.fecha.slice(0, 10) === isoDate);
            if (eventForDay.length) {
                const dot = document.createElement('span');
                dot.classList.add('event-dot');
                button.appendChild(dot);
                button.classList.add('has-event');
            }

            if (isoDate === new Date().toISOString().slice(0, 10)) {
                button.classList.add('today');
            }

            button.addEventListener('click', () => selectDate(isoDate));
            daysContainer.appendChild(button);
        }

        if (!selectedDate) {
            selectDate(new Date().toISOString().slice(0, 10));
        }
    }

    function selectDate(dateString) {
        selectedDate = dateString;
        document.querySelectorAll('.calendar-day').forEach(btn => btn.classList.toggle('selected', btn.dataset.date === dateString));
        renderEventsForDate(dateString);
        eventDate.value = dateString;
    }

    function renderEventsForDate(dateString) {
        const events = allEvents.filter(event => event.fecha.slice(0, 10) === dateString);
        eventList.innerHTML = '';

        if (events.length === 0) {
            eventList.innerHTML = '<p class="text-muted">No hay eventos registrados para esta fecha.</p>';
            return;
        }

        events.forEach(event => {
            const item = document.createElement('div');
            item.classList.add('event-item');
            item.innerHTML = `
                <h5>${event.nombre}</h5>
                <p>${event.descripcion || 'Sin descripción'}</p>
                <p class="event-location"><i class="fas fa-map-marker-alt"></i> ${event.ubicacion || 'Ubicación por confirmar'}</p>
            `;
            eventList.appendChild(item);
        });
    }

    if (!authNotice) {
        eventForm.classList.remove('disabled-form');
        eventForm.querySelectorAll('input, textarea, button').forEach(el => el.disabled = false);
    }

    prevButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        buildCalendar(currentDate);
    });

    nextButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        buildCalendar(currentDate);
    });

    buildCalendar(currentDate);
});
