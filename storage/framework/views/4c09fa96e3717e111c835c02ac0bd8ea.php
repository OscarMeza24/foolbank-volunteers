<!DOCTYPE html>
<html lang="<?php echo e(str_replace('_', '-', app()->getLocale())); ?>">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title><?php echo e(config('app.name', 'Foodbank Volunteers')); ?></title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100">
        <div class="min-h-screen flex items-center justify-center">
            <div class="max-w-4xl w-full space-y-8 p-8 bg-white rounded-lg shadow-md">
                <div class="text-center">
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">
                        Bienvenido a Foodbank Volunteers
                    </h1>
                    <p class="text-gray-600">
                        Sistema de gestión de voluntarios para bancos de alimentos
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">
                            Gestión de Eventos
                        </h2>
                        <p class="text-gray-600">
                            Crea y gestiona eventos de distribución de alimentos
                        </p>
                    </div>
                    <div class="p-6">
                        <h2 class="text-xl font-semibold text-gray-900 mb-4">
                            Gestión de Voluntarios
                        </h2>
                        <p class="text-gray-600">
                            Recruta y gestiona voluntarios para tus eventos
                        </p>
                    </div>
                </div>

                <?php if(auth()->guard()->check()): ?>
                    <div class="text-center">
                        <a href="<?php echo e(route('events.index')); ?>" class="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Ir a Eventos
                        </a>
                        <a href="<?php echo e(route('volunteers.index')); ?>" class="inline-block bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-4">
                            Ir a Voluntarios
                        </a>
                    </div>
                <?php else: ?>
                    <nav class="flex items-center justify-end gap-4">
                        <a
                            href="<?php echo e(route('login')); ?>"
                            class="inline-block px-5 py-1.5 dark:text-[#EDEDEC] text-[#1b1b18] border border-transparent hover:border-[#19140035] dark:hover:border-[#3E3E3A] rounded-sm text-sm leading-normal"
                        >
                            Iniciar Sesión
                        </a>
                        <a
                            href="<?php echo e(route('register')); ?>"
                            class="inline-block px-5 py-1.5 dark:text-[#EDEDEC] border-[#19140035] hover:border-[#1915014a] border text-[#1b1b18] dark:border-[#3E3E3A] dark:hover:border-[#62605b] rounded-sm text-sm leading-normal"
                        >
                            Registrarse
                        </a>
                    </nav>
                <?php endif; ?>
            </div>
        </div>
    </body>
</html><?php /**PATH C:\Users\USER PC\foodbank-volunteers\resources\views/welcome.blade.php ENDPATH**/ ?>