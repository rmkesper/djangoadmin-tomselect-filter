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
        const fullUrl = `${url}&q=${encodeURIComponent(query)}`;
        fetch(fullUrl)
          .then((res) => res.json())
          .then((json) => callback(json))
          .catch(() => callback());
      },
      onChange: function () {
        const values = el.tomselect.getValue();
        const searchParams = new URLSearchParams(window.location.search);
        if (values.length) {
          searchParams.set(param, values.join(","));
        } else {
          searchParams.delete(param);
        }
        window.tomselect_query = searchParams.toString();
      },
      onFocus: function() {
        if (!this.input.value && this.items.length === 0) {
          this.load('');
        }
      }
    });

    const initialValues = getUrlParameter(param);  // adjust param name
    if (initialValues.length > 0) {
      const url = select.input.getAttribute('data-url');
      fetch(`${url}&q=${initialValues.join(',')}`) // TODO
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
