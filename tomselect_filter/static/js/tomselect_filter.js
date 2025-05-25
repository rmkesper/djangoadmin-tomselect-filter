document.addEventListener("DOMContentLoaded", function () {
  function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.getAll(name);
  }

  if (!window.tomselect_query) {
    window.tomselect_query = ""
  }

  document.querySelectorAll(".tom-select-filter").forEach((el) => {
    const url = el.dataset.url;
    const param = el.dataset.param;

    const select = new TomSelect(el, {
      valueField: "value",
      labelField: "label",
      searchField: "label",
      create: false,
      plugins: ['remove_button'],
      load: function (query, callback) {
        const fullUrl = `${url}&q=${encodeURIComponent(query)}&query=${encodeURIComponent(window.location.search)}`;
        fetch(fullUrl)
          .then((res) => res.json())
          .then((json) => callback(json))
          .catch(() => callback());
      },
      onChange: function () {
        const values = el.tomselect.getValue();
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.delete(param);
        values.forEach(val => {
          searchParams.append(param, val);
        });
        window.tomselect_query = searchParams.toString();
      },
      onFocus: function() {
        if (!this.input.value && this.items.length === 0) {
          this.load('');
        }
      }
    });

    let initialValues = getUrlParameter(param);
    if (initialValues.length == 1) {
        initialValues = initialValues[0].split(",")
    }
    if (initialValues.length > 0) {
      const url = select.input.getAttribute('data-url');
      fetch(`${url}&q=${initialValues.join(',')}&query=${encodeURIComponent(window.location.search)}`)
        .then(res => res.json())
        .then(data => {
          data.forEach(item => {
            // add option if not already present
            if (!select.options.hasOwnProperty(item.value)) {
              select.addOption(item);
            }
          });
          select.setValue(initialValues);
        });
    }

    const submit_btn = document.querySelector(`#submit_${param}`);
    if (submit_btn) {
      submit_btn.addEventListener("click", function () {
        if (window.tomselect_query) {
          window.location.search = window.tomselect_query;
        }
      });
    }
  });
});
