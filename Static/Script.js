document.addEventListener('DOMContentLoaded', function() {
    
   
    const splash = document.getElementById('splash-screen');
    if (splash) {
 
        if (sessionStorage.getItem('splash_visualizada')) {
            splash.style.display = 'none'; 
        } else {

            setTimeout(function() {
                splash.classList.add('hidden-splash');
                sessionStorage.setItem('splash_visualizada', 'true');
                setTimeout(() => splash.style.display = 'none', 300);
            }, 2000);
        }
    }


    const btnTheme = document.getElementById('theme-toggle');
    if (btnTheme) {
        btnTheme.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const newTheme = isDark ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }


    const btnLimpar = document.getElementById('btnLimparMaster');
    const menuLimpeza = document.getElementById('menuLimpeza');
    if (btnLimpar) {
        btnLimpar.addEventListener('click', (e) => {
            e.stopPropagation();
            menuLimpeza.classList.toggle('show');
        });
        document.addEventListener('click', () => menuLimpeza.classList.remove('show'));
    }


    const desenhar = (canvasId, type, scriptId) => {
        const canvas = document.getElementById(canvasId);
        const dataTag = document.getElementById(scriptId);
        

        if (canvas && dataTag) {
            const dados = JSON.parse(dataTag.textContent);
            if (Object.keys(dados).length === 0) {
                canvas.parentElement.innerHTML = "<p style='text-align:center; padding-top:40px; color:#888;'>Sem dados.</p>";
                return;
            }

            new Chart(canvas.getContext('2d'), {
                type: type,
                data: {
                    labels: Object.keys(dados),
                    datasets: [{
                        data: Object.values(dados),
                        backgroundColor: ['#1b4332', '#2d6a4f', '#40916c', '#52b788', '#74c69d', '#95d5b2'],
                        borderWidth: 2,
                        borderColor: 'transparent'
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: { legend: { display: (type === 'doughnut'), position: 'bottom' } }
                }
            });
        }
    };


    desenhar('graficoPizzaHome', 'doughnut', 'dados-grafico-json');
    desenhar('graficoPizzaPagina', 'doughnut', 'dados-pizza');      
    desenhar('graficoBarraPagina', 'bar', 'dados-anual');           
});
