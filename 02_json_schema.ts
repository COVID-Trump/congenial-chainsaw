interface QuestionBase {
    type: 'choice' | 'mul_choice' | 'fill_int' | 'fill_float'
    answers: any[]
}

interface Choice extends QuestionBase {
    type: 'choice'
    answers: string[]
    choices: string[]   // choices that are never selected do NOT exist here in the samples
}

interface MultipleChoice extends QuestionBase {
    type: 'mul_choice'
    answers: string[][]
    choices: string[]   // choices that are never selected do NOT exist here in the samples
}

interface FillInt extends QuestionBase {
    type: 'fill_int'
    answers: number[]   // ints
}

interface FillFloat extends QuestionBase {
    type: 'fill_float'
    answers: number[]   // floats
}

type Question = Choice | MultipleChoice | FillInt | FillFloat

export type JsonReport = Question[];
