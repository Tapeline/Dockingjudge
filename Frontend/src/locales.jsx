import LocalizedStrings from 'react-localization';

let locales = new LocalizedStrings({
    en: {
        helpPage: {
            title: "Help",
            titleVerdicts: "Verdicts",
            subtitleVerdicts: "Testing system answers explanation",
            columnCode: "Verdict code",
            columnShort: "Name",
            columnDesc: "Full description",
            verdictNCShort: "Not Checked",
            verdictNCDesc: "Solution is waiting for it to be checked",
            verdictOKShort: "Accepted",
            verdictOKDesc: "Everything's fine, your solution is fully functional",
            verdictWAShort: "Wrong Answer",
            verdictWADesc: "Your solution gives a wrong answer at some moment",
            verdictREShort: "Runtime Error",
            verdictREDesc: "Your program exits with error",
            verdictPEShort: "Presentation Error",
            verdictPEDesc: "Your program gives answer in the wrong format",
            verdictPCFShort: "Precompile Checks Failed",
            verdictPCFDesc: "Your solution failed to match prerequisites",
            verdictTLShort: "Too Long / Time Limit",
            verdictTLDesc: "Your program has exceeded the time limit",
            verdictMLShort: "Memory Limit",
            verdictMLDesc: "Your program has exceeded the memory limit",
            verdictTSFShort: "Testing System Failed",
            verdictTSFDesc: "Indicates an internal error in testing system. Report to admin immediately"
        }
    },
    ru: {
        helpPage: {
            title: "Помощь",
            titleVerdicts: "Вердикты",
            subtitleVerdicts: "Пояснения к ответам тестирующей системы",
            columnCode: "Код вердикта",
            columnShort: "Название",
            columnDesc: "Описание",
            verdictNCShort: "Непроверено",
            verdictNCDesc: "Решение ожидает проверки",
            verdictOKShort: "Принято",
            verdictOKDesc: "Решение верно",
            verdictWAShort: "Неверный ответ",
            verdictWADesc: "Решение выдает неверный ответ на одном из тестов",
            verdictREShort: "Ошибка исполнения",
            verdictREDesc: "Решение падает с ошибкой исполнения",
            verdictPEShort: "Ошибка формата",
            verdictPEDesc: "Решение выдает ответ в неверном формате",
            verdictPCFShort: "Предкомпиляционные проверки не пройдены",
            verdictPCFDesc: "Решение не соответствует описанным в задаче требованиям",
            verdictTLShort: "Лимит времени",
            verdictTLDesc: "Решение выполнялось слишком долго и было прервано",
            verdictMLShort: "Лимит памяти",
            verdictMLDesc: "Решение занимало слишком много памяти и было прервано",
            verdictTSFShort: "Ошибка тестирующей системы",
            verdictTSFDesc: "Сообщает о внутренней ошибке тестирующей смистемы"
        }
    }
});

export default locales;
