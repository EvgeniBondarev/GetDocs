
        (function() {
            'use strict';

            const imgBg = document.createElement('div');
            document.getElementsByTagName('body')[0].appendChild(imgBg);
            imgBg.style = 'background-color: rgba(48, 48, 48, 0.6); position: fixed; top: 0px; left: 0px; width: 100%; z-index: 1';
            imgBg.hidden = true;
            fillBg();
            window.addEventListener('resize', fillBg);

            let bigImgageScreenFraction;
            if (window.matchMedia('(max-width: 1080px)').matches) {
                bigImgageScreenFraction = 4;
            } else {
                bigImgageScreenFraction = 2;
            }

            let placeholder = document.createElement('img');
            document.querySelectorAll('img[scalable]').forEach((img) => {
                const smallSize = img.getAttribute('scalable');
                let defaultStyle = `max-width: ${smallSize}; max-height: ${smallSize}`;
                img.style = defaultStyle;
                let isGoingToSmall = false;
                img.addEventListener('click', () => {
                    if (img.getAttribute('is-big') === 'true') {
                        let coords = placeholder.getBoundingClientRect();
                        img.style = `${defaultStyle}; position: fixed; left: ${coords.left}px; top: ${coords.top}px`;
                        img.setAttribute('is-big', false);
                        imgBg.hidden = true;
                        isGoingToSmall = true;
                    } else {
                        imgBg.hidden = false;
                        img.setAttribute('is-big', true);
                        placeholder.hidden = false;
                        placeholder.style = `width: ${img.width}px; height: ${img.height}px; background-color: rgb(255, 255, 255)`;
                        img.before(placeholder);
                        doImageBig(img);
                    }
                });
                img.addEventListener('transitionend', () => {
                    if (isGoingToSmall) {
                        img.style = defaultStyle;
                        isGoingToSmall = false;
                        placeholder.hidden = true;
                    }
                });
                window.addEventListener('resize', () => {
                    if (img.getAttribute('is-big') === 'true') doImageBig(img);
                });
            });

            function fillBg() {
                imgBg.style.height = (document.documentElement.clientHeight + 100) + 'px';
            }

            function doImageBig(img) {
                let screenHeight = document.documentElement.clientHeight;
                let screenWidth = document.documentElement.clientWidth;
                let imgWidth = img.width;
                let imgHeight = img.height;
                let bigImgHeight = Math.round(imgHeight * bigImgageScreenFraction);
                let bigImgWidth = Math.round(imgWidth * bigImgageScreenFraction);
                let left = Math.round(0.5 * (screenWidth - bigImgWidth));
                let top = Math.round(0.5 * (screenHeight - bigImgHeight));
                img.style = `width: ${bigImgWidth}px; height: ${bigImgHeight}px; left: ${left}px; top: ${top}px; position: fixed; z-index: 2`;
            }
        })();
