import { render } from '@testing-library/react';

// --- SIMULAÇÃO DA REGRA DE NEGÓCIO ---
// Em um cenário real, você importaria isso de: import { calculateYield } from './utils';
// A regra é: Produtividade = Produção Total / Área Plantada
const calculateYield = (production: number, area: number) => {
  if (area <= 0) {
    throw new Error("A área deve ser maior que zero");
  }
  // Retorna com 2 casas decimais
  return parseFloat((production / area).toFixed(2));
};

// --- SUÍTE DE TESTES ---
describe('Regras de Negócio: Gestão Agrícola', () => {

  // Cenário 1: O Caminho Feliz (Happy Path)
  it('deve calcular a produtividade padrão corretamente', () => {
    const production = 1000; // Toneladas
    const area = 10;         // Hectares

    // Esperado: 100 Ton/Ha
    expect(calculateYield(production, area)).toBe(100);
  });

  // Cenário 2: Precisão Decimal
  it('deve lidar com dízimas periódicas arredondando corretamente', () => {
    const production = 100;
    const area = 3;

    // 100 dividio por 3 é 33.33333... queremos apenas 33.33
    expect(calculateYield(production, area)).toBe(33.33);
  });

  // Cenário 3: Proteção contra Falhas (Edge Case)
  it('NÃO deve permitir divisão por zero (área inválida)', () => {
    // Aqui testamos se o sistema "explode" do jeito certo quando o usuário erra
    expect(() => calculateYield(500, 0)).toThrow("A área deve ser maior que zero");
  });

});
