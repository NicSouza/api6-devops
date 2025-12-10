import { render } from '@testing-library/react';


const calculateYield = (production: number, area: number) => {
  if (area <= 0) {
    throw new Error("A área deve ser maior que zero");
  }
  return parseFloat((production / area).toFixed(2));
};

describe('Regras de Negócio: Gestão Agrícola', () => {

  it('deve calcular a produtividade padrão corretamente', () => {
    const production = 1000;
    const area = 10;

    expect(calculateYield(production, area)).toBe(100);
  });

  it('deve lidar com dízimas periódicas arredondando corretamente', () => {
    const production = 100;
    const area = 3;

    expect(calculateYield(production, area)).toBe(33.33);
  });

  it('NÃO deve permitir divisão por zero (área inválida)', () => {
    expect(() => calculateYield(500, 0)).toThrow("A área deve ser maior que zero");
  });

});
