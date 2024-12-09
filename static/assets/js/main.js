(function ($) {
    /* 
        Toggle 'open' class on click of element with class 'ps-hasmenu'
    */
    $(document).on("click", ".ps-hasmenu>.ps-link", function (e) {
        e.preventDefault();

        if ($(this).parent().hasClass("open-menu")) {
            $(this).parent().find(".ps-submenu").slideUp();
        } else {
            $(this).parent().find(".ps-submenu").slideDown();
        }

        $(this).parent().toggleClass("open-menu");
    });

    $(document).ready(function () {
        $(document).find(".ps-item").removeClass("active");
        $(document).find(".ps-hasmenu").removeClass("open-menu active");
        const pathname = window.location.pathname;

        if (pathname) {
            const fineEle = $(document).find("a[href='" + pathname + "']");
            if (fineEle.length > 0) {
                fineEle.addClass("active");

                if (fineEle.closest("ul").hasClass("ps-submenu")) {
                    fineEle.closest(".ps-hasmenu").addClass("open-menu active");
                    fineEle.closest(".ps-submenu").slideDown();
                } else {
                    fineEle.closest(".ps-item").addClass("active");
                }
            }
        }
    });


    /* 
        Toggle 'ps-sidebar-hide' class on click of element with id 'sidebar-hide'
    */
    $(document).on("click", "#sidebar-hide", function (e) {
        e.preventDefault();
        $('.ps-sidebar').toggleClass("ps-sidebar-hide");
    })

    /* 
        Toggle 'mob-sidebar-active' class and show/hide menu overlay on click of element with id 'mobile-collapse'
    */
    $(document).on("click", "#mobile-collapse", function (e) {
        e.preventDefault();
        $('.ps-sidebar').toggleClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").toggleClass("d-none");
    })

    /* 
        Hide mobile sidebar and menu overlay on click of element with class 'ps-menu-overlay'
    */
    $(document).on("click", ".ps-menu-overlay", function (e) {
        e.preventDefault();
        $('.ps-sidebar').removeClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").addClass("d-none");
    })

    $(document).ready(function () {
        try {
            $(document).find('select:not(.noselect2):not(.inmodal)').each(function () {
                $(this).select2();
            });

            $(document).find('select.inmodal:not(.noselect2)').each(function () {
                $(this).select2({
                    dropdownParent: $(this).closest(".modal")
                });
            });
        } catch (error) {
            console.log(error);
        }
    });


    const tinymceSelector = $(document).find(".tinymce");
    if (tinymceSelector.length > 0) {
        tinymce.init({
            selector: '.tinymce',
            promotion: false,
            license_key: 'gpl', // Agree to GPL terms
            menubar: true,
            plugins: "codesample link media image code fullscreen table autolink advlist lists autoresize emoticons wordcount",
            toolbar: [
                'bold italic underline strikethrough | subscript superscript | list bullist numlist blockquote alignleft aligncenter alignright alignjustify autolink link table',
                'formatselect autolink forecolor | subscript superscript | outdent indent | image media emoticons | wordcount codesample fullscreen code'
            ],
            image_advtab: false,
            relative_urls: false,
            remove_script_host: true,
            toolbar_sticky: true,
            image_dimensions: false,
            image_class_list: [
                { title: 'Responsive', value: 'img-responsive' }
            ],
            table_class_list: [
                { title: 'Table Bordered', value: 'table table-bordered' },
                { title: 'None', value: '' }
            ],
            noneditable_noneditable_class: 'alert',
            min_height: 300
        });
    }

    const datatableElement = $(document).find('.datatable');
    if (datatableElement.length > 0) {
        try {
            datatableElement.DataTable({
                paging: true,
                lengthChange: true,
                searching: true,
                ordering: false,
                info: true,
                autoWidth: false,
                responsive: true,
            });
        } catch (error) {
            console.log(error);
        }
    }
    $(document).ready(function () {
        const datatableAjaxElement = $(document).find('.ajaxdatatable');
        if (datatableAjaxElement.length > 0) {
            try {
                datatableAjaxElement.DataTable({
                    lengthChange: true,
                    serverSide: true,
                    order: [],
                    ajax: {
                        url: datatableAjaxElement.data("ajax"),
                        type: 'GET'
                    },
                    drawCallback: function (dt) {

                    },
                    language: {
                        emptyTable: datatableAjaxElement.data("nodata") ?? 'No data available'
                    },
                    processing: true,
                    errorCallback: function (settings, xhr, errorthrown) {
                        console.error('DataTables Ajax error:', errorthrown);
                    }
                });
            } catch (error) {
                console.log(error);
            }
        }
    });

    $(document).on('click', '.password_field .show-hide', function () {
        const parentEle = $(this).parent();
        if (parentEle.length > 0) {
            const prevType = parentEle.find("input").attr("type");
            if (prevType == 'password') {
                parentEle.find("input").attr("type", "text");
                parentEle.find("input").attr("placeholder", "Password");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye"></i>');
            } else {
                parentEle.find("input").attr("type", "password");
                parentEle.find("input").attr("placeholder", "********");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye-slash"></i>');
            }
        }
    });
    window.onFileHubCallback = (file, id) => {
        try {
            const findImageEle = $(document).find(`[name="${id}"]`);
            if (findImageEle.length > 0) {
                const fileExt = file.uri.split('.').pop().toLowerCase();
                const imageExtensions = ['png', 'jpg', 'jpeg', 'svg', 'webp', 'gif', 'bmp'];

                findImageEle.val(file.uri).trigger("change");

                const container = findImageEle.closest(".image_picker_container");
                if (container) {
                    container.addClass("added");
                    container.find(".image_fill_placeholder").remove();

                    if (imageExtensions.includes(fileExt)) {
                        container.append(`
                        <div class="image_fill_placeholder mt-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                                <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                                      stroke-width="32" d="M368 368L144 144M368 144L144 368"></path>
                            </svg>
                            <img src="${file.uri}" style="width:auto;max-width:100%;" alt="Preview File"/>
                        </div>
                    `);
                    } else {
                        const fileName = file.uri.split('/').pop();
                        container.append(`
                        <div class="image_fill_placeholder mt-2" style="border: 2px solid #eeeeee;border-radius: 10px;padding: 10px;">
                            <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                                <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                                      stroke-width="32" d="M368 368L144 144M368 144L144 368"></path>
                            </svg>
                            
                            <div class="file_card" style="display: flex;align-items: center;gap: 10px;">
                                <img style="width:50px;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAACx0lEQVR4nO2bu2sVQRTGfzHgg2gaG41YmitYirGwFgTFFDYWuQFRY2HjK/ioJFhEbQQhGAOCCP4BaqcWtoqFiFWuNiqIYHwWBgNXBubCYVjjZvfM7sy988HhLlz2O+d8O68zuwPVYwAYBc4A55VtAthOoOgDJoFvQNuzPQUaBIRVwP0KEpf2FRghEEw6wbWAWWBa0a4DD4E/ws9HYEPdyQ84zX4OWOPRn3nqC8LfRWrGQRHMvOfkOzgufL6oaoA7BBy21xJnRTC3qggGGBI+f/h2thq4KxyOO/9fFv+Z66ogxxxv2Ag8c5wd7RUBhm2flo5u2imv6wXYA3wWDpbsSiwLXSfAEWBRkP+yIz3dLkCfk0xnobHzP/d1hQBrM5ayr4CtOe6NXoBNwHOH8AGwPuf9UQswCLxxyG4A/SvgiFqAK85If7IAR9QCzAuSEwU5ZgWH2QSJSoDfgsR0hyKD5zvBsZ/IBPggSPYVSP6OuN+UqOuITIAZZ8Ezk3Nv7rbz5I2dolqoCDAEfFpm2ymv3csok6NZB+wAXhdMfME++aqTV18J9gN77d5env2508CBivt85eVw6EgCkFoAqQtQcgy4Zuf/q/RoF1i0BOa3JwVoFyAxm6JND29+mxkbrtqxq5CMK6wc/2VGhOAFaHoUYMxz7GpdYEz5ze+05YyiC4SCJACpBZC6ADWMAcMZu0Ea9hbY5jl2FZJzHqdB87FFFC2g5SH5ViwtIBQkAUgtgNQFqKkWaKZyGC/TYCqH8dt61bpAKocDQJoGSdMgaR1AqgVIxRB1j6Q1IQ2CKDy8n4JkM/Fgi4j7exmil4LoGPFgQuvQ1CVB9CWkg4jLYLdzbO5CGbJBeyagQ2YOJT4CpjyUu2Vtysa2JOJ9r3FwcsQeQ21HZibmXSihATwJIKm89tjuTqujYU9lms/etd/+ljUTk4ltRYn/BZi9S5cZIajtAAAAAElFTkSuQmCC" alt="File Icon" />
                                <div class="file_info">
                                    <div class="file_name">${fileName}</div>
                                    <div class="file_size" style="color:#ccc;">Size: ${file.size || 'Unknown'}</div>
                                </div>
                            </div>
                        </div>
                    `);
                    }
                }
            }
        } catch (error) {
            console.log(error);
        }
        $.fancybox.close();
    };


    function init_fancybox() {
        const fancyboxfile = $(document).find(".openImagePicker");
        if (fancyboxfile.length > 0) {
            fancyboxfile.fancybox({
                width: 900,
                height: 300,
                type: 'iframe',
                autoScale: false
            });
        }
    }

    init_fancybox();

    $(document).on("click", ".image_picker_container svg", function () {
        const container = $(this).closest(".image_picker_container");
        container.removeClass("added");
        container.find(".image_fill_placeholder").remove();
        container.find("input").val("");
    });
    $(document).on("click", ".sameAsPermanent", function () {
        const address = $(document).find("[name='permanent-address']").val();
        const city = $(document).find("[name='permanent-city']").val();
        const province = $(document).find("[name='permanent-province']").val();
        const country = $(document).find("[name='permanent-country']").val();
        const postcode = $(document).find("[name='permanent-postcode']").val();
        const contactnumber = $(document).find("[name='permanent-contact_number']").val();

        console.log(address, city, province, country, postcode, contactnumber);

        $(document).find("[name='temporary-address']").val(address);
        $(document).find("[name='temporary-city']").val(city);
        $(document).find("[name='temporary-province']").val(province);
        $(document).find("[name='temporary-country']").val(country);
        $(document).find("[name='temporary-postcode']").val(postcode);
        $(document).find("[name='temporary-contact_number']").val(contactnumber);
    })
})(jQuery);